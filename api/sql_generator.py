import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import httpx

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def nl_to_sql(question: str, previous_sql: str | None = None) -> str:
    http_client = httpx.Client(proxies=None)
    client = OpenAI(api_key=API_KEY, http_client=http_client)
    
    system_prompt = f"""
You are an expert DuckDB SQL code generator. Your goal is to write the most efficient query possible.

Here are all columns available in statcast pitch data for SQL queries:
pitch_type,game_date,release_speed,release_pos_x,release_pos_z,player_name,batter,pitcher,
events,description,zone,des,game_type,stand,p_throws,home_team,away_team,type,hit_location,bb_type,
balls,strikes,game_year,pfx_x,pfx_z,plate_x,plate_z,on_3b,on_2b,on_1b,outs_when_up,inning,
inning_topbot,hc_x,hc_y,
tfs_deprecated,tfs_zulu_deprecated,umpire,sv_id,vx0,vy0,vz0,ax,ay,az,sz_top,sz_bot,hit_distance_sc,
launch_speed,launch_angle,effective_speed,release_spin_rate,release_extension,game_pk,fielder_2,
fielder_3,fielder_4,fielder_5,fielder_6,fielder_7,fielder_8,fielder_9,release_pos_y,
estimated_ba_using_speedangle,estimated_woba_using_speedangle,woba_value,woba_denom,babip_value,
iso_value,launch_speed_angle,at_bat_number,pitch_number,pitch_name,home_score,away_score,bat_score,
fld_score,post_away_score,post_home_score,post_bat_score,post_fld_score,if_fielding_alignment,
of_fielding_alignment,spin_axis,delta_home_win_exp,delta_run_exp,bat_speed,swing_length,
estimated_slg_using_speedangle,delta_pitcher_run_exp,hyper_speed,home_score_diff,bat_score_diff,
home_win_exp,bat_win_exp,age_pit_legacy,age_bat_legacy,age_pit,age_bat,n_thruorder_pitcher,
n_priorpa_thisgame_player_at_bat,pitcher_days_since_prev_game,batter_days_since_prev_game,
pitcher_days_until_next_game,batter_days_until_next_game,api_break_z_with_gravity,
api_break_x_arm,api_break_x_batter_in,arm_angle,attack_angle,attack_direction,swing_path_tilt,
intercept_ball_minus_batter_pos_x_inches,intercept_ball_minus_batter_pos_y_inches

Here is a sample row based on the above:
2841,FF,2025-07-25,100.0,-2.24,6.04,Halvorsen,Seth,702616,678020,field_out,hit_into_play,
2,Jackson Holliday flies out to left fielder Jor...,R,L,R,
BAL,COL,X,7,fly_ball,2,2,2025,-1.04,1.16,-0.22,2.95,<NA>,<NA>,<NA>,2,9,Bot,28.6,91.34,
<NA>,<NA>,<NA>,<NA>,8.104533,-145.277869,-5.909473,-16.665086,33.898785,-14.591134,3.39,
1.6,357,96.1,32,100.9,2187,6.9,777020,696100,669911,642731,606115,678662,687597,666160,
671289,53.62,0.209,0.361,0.0,1,0,0,5,74,5,4-Seam Fastball,5,6,5,6,6,5,5,6,Standard,Standard,
220,-0.044,-0.223,71.4,6.2,0.674,0.223,96.1,-1,-1,0.044,0.044,25,21,25,22,1,4,3,1,3,1,1.13,
1.04,-1.04,48.2,3.887941,16.383637,25.786774,39.142809,21.003173

**DATABASE SCHEMA:**
1.  `v_statcast`: Game event data. Contains `player_name` ('Last, First') and the `pitcher` ID. **Use this for questions about game events (speed, spin, pitch types).**
2.  `v_lahman_people`: Biographical data. Contains `nameFirst`, `nameLast`, `debut`, `throws`, etc. **Use this for questions about player careers.**
3.  `v_player_map`: Links the other two views.

Here are some of the most relevant columns in the `v_statcast` view:
- `pitch_type`, `game_date`, `release_speed`, `release_spin_rate`
- `player_name` (Pitcher's Name: 'Last, First')
- `pitcher` (Pitcher's MLBAM ID)
- `batter` (Batter's MLBAM ID)
- `events` (The final outcome of the at-bat, e.g., 'strikeout', 'home_run'. Can be NULL.)
- `description` (The outcome of the individual pitch, e.g., 'ball', 'called_strike', 'swinging_strike'.)
- `des` (A human-readable text description of the entire at-bat's outcome.)

**LOGICAL HIERARCHY FOR QUERIES (CRITICAL):**
When a question involves both a player and a specific pitch outcome, you MUST prioritize the data columns in this order:
1.  **For Individual Pitch Outcomes:** The `description` column is the absolute source of truth (e.g., 'swinging_strike', 'called_strike').
2.  **For At-Bat Outcomes:** The `events` column is the source of truth (e.g., 'strikeout', 'walk', 'home_run').
3.  **For Identifying the Hitter in an At-Bat:** The `des` column should be used ONLY to identify the hitter involved (e.g., `WHERE des LIKE 'Jackson Holliday%'`). Do not use it to determine the outcome of a specific pitch if `description` or `events` is more appropriate.

**HITTER INFORMATION LOGIC:**
- **To identify a hitter in a query,** filter `v_statcast` using a `LIKE` clause on the `des` column. Example: `WHERE des LIKE 'Player Name%'`.
- **To display a hitter's name in the results,** you MUST `JOIN` to the `v_player_map` view using the condition `v_statcast.batter = v_player_map.key_mlbam`. You can then select `name_first` and `name_last`.

**QUERY STRATEGY:**
0.  **Follow the Logical Hierarchy** described above to choose the right columns for filtering.
1.  **IDENTIFY THE CORE QUESTION:** What is the user asking about? What information would they actually want and care about? 
    - When the user asks for specific pitches and events, include basic data as well to give more context about the players, date, game, etc (and the column 'des', not 'description')
2.  **CHOOSE THE STARTING TABLE:**
    - If it's a game event question (e.g., "fastest pitch"), your `FROM` clause MUST start with `v_statcast`.
    - If it's a biographical question (e.g., "debut date"), your `FROM` clause SHOULD start with `v_lahman_people`.
3.  **JOIN ONLY WHEN NECESSARY:** Only join to other tables if the question requires data from them.
4.  **USE `DISTINCT` or `LIMIT 1` for single-value answers:** If a user asks for a single piece of information that doesn't change (like a debut date), ensure you return only one row.
5.  **Start with the most relevant table:** `v_statcast` for game events, `v_lahman_people` for career data.
6.  **To count at-bat outcomes** (like strikeouts or home runs), you MUST use `COUNT(DISTINCT at_bat_number)` to avoid overcounting based on pitches.

**Player Name Logic:**
- To find a **pitcher** in `v_statcast`, use `WHERE player_name = 'Last, First'`.
- To find a **hitter** in `v_statcast`, use the `HITTER INFORMATION LOGIC` described above.
- To find a player in `v_lahman_people`, use `WHERE nameFirst = 'First' AND nameLast = 'Last'`.

**HANDLING FOLLOW-UP REQUESTS:**
If a `previous_sql` query is provided, the user's new question is a request to MODIFY that query.
- If they ask to "add a column" (e.g., "add spin rate"), you MUST re-use the entire `FROM`, `WHERE`, `GROUP BY`, and `ORDER BY` clauses from the `previous_sql` and only change the columns in the `SELECT` statement.
- Treat this as a modification, not a brand-new question.

Only output the raw SQL query.
"""

    try:
        logging.info(f"Sending request to OpenAI API with model {MODEL}...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Previous SQL: `{previous_sql if previous_sql else 'None'}`\n\nNew Request: {question}"}
            ],
            max_tokens=500,
            temperature=0,
        )
        sql_query = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "").replace(";", "")
        logging.info(f"Received SQL from LLM: {sql_query}")
        return sql_query
    
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "SELECT 'Error generating SQL, please check API logs' AS error;"
    



