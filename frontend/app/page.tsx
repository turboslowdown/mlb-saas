"use client";

import { useState, useMemo } from 'react';
import { FaArrowUp } from 'react-icons/fa';
import SimpleBarChart from './components/BarChart';

interface QueryResult {
  sql_query: string;
  results: Record<string, string | number | boolean | null>[];
}

const getVisualizationType = (results: Record<string, any>[] | undefined): 'barchart' | 'table' => {
    if (!results || results.length === 0) {
      return 'table';
    }
    const firstRow = results[0];
    const keys = Object.keys(firstRow);
    if (
        keys.length === 2 &&
        typeof firstRow[keys[0]] === 'string' &&
        typeof firstRow[keys[1]] === 'number'
    ) {
        return 'barchart';
    }
    return 'table';
};

export default function HomePage() {
  const [question, setQuestion] = useState<string>('');
  // MODIFICATION: Removed unused 'queryResult' state
  const [lastSuccessfulResult, setLastSuccessfulResult] = useState<QueryResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'ascending' | 'descending' } | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!question.trim()) return;
    setIsLoading(true);
    setError(null);

    try {
      const requestBody = {
        question: question,
        previous_sql: lastSuccessfulResult ? lastSuccessfulResult.sql_query : null,
      };

      const response = await fetch(process.env.NEXT_PUBLIC_API_URL + '/query', { // Using the environment variable
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      const data: QueryResult = await response.json();
      setLastSuccessfulResult(data);
      setQuestion('');
      setSortConfig(null);

    } catch (err) { // MODIFICATION: Explicitly typed 'err'
      const error = err as Error;
      setError(error.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setLastSuccessfulResult(null);
    setQuestion('');
    setError(null);
    setSortConfig(null);
  };

  const sortedResults = useMemo(() => {
    if (!lastSuccessfulResult || !lastSuccessfulResult.results) {
      return [];
    }
    // MODIFICATION: Changed 'let' to 'const'
    const sortableItems = [...lastSuccessfulResult.results];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        const valA = a[sortConfig.key];
        const valB = b[sortConfig.key];
        if (valA === null || valA === undefined) return 1;
        if (valB === null || valB === undefined) return -1;
        if (valA < valB) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (valA > valB) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [lastSuccessfulResult, sortConfig]);

  const handleSort = (key: string) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };
  
  const visualizationType = getVisualizationType(lastSuccessfulResult?.results);
  const hasInput = question.trim().length > 0;


  return (
    <main
      className="flex flex-col items-center min-h-screen w-full bg-cover bg-center bg-no-repeat p-8 font-sans"
      style={{ backgroundImage: "url('/stadium-bg.jpg')" }}
    >
      <div className="flex flex-col justify-center items-center w-full max-w-3xl mx-auto flex-grow">
        {/* Logo */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold text-white tracking-wider">FULLCOUNT</h1>
          <div className="flex justify-center items-center space-x-2 mt-2">
            <div className="w-6 h-6 rounded-full bg-transparent border-4 border-white"></div>
            <div className="w-6 h-6 rounded-full bg-transparent border-4 border-white"></div>
            <div className="w-6 h-6 rounded-full bg-transparent border-4 border-white"></div>
            <div className="w-6 h-6 rounded-full bg-yellow-400"></div>
            <div className="w-6 h-6 rounded-full bg-yellow-400"></div>
          </div>
        </div>

        {/* Search Form */}
        <div className="w-full relative">
          <form onSubmit={handleSubmit} className="mb-4 relative flex items-center">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask any question about baseball from 2015-now"
              className="w-full p-4 pl-6 pr-16 rounded-full text-lg text-white placeholder-gray-400 
                        bg-[rgba(55,65,81,0.57)] border border-[rgba(209,213,219,0.28)] 
                        focus:outline-none focus:ring-2 focus:ring-yellow-400/80
                        transition-shadow duration-300 ease-in-out backdrop-blur-sm"
              disabled={isLoading}
            />
            {/* MODIFICATION: Removed top-1/2 -translate-y-1/2 for better centering with flex */}
            <button
              type="submit"
              disabled={isLoading || !hasInput}
              className={`absolute right-2 w-12 h-12 rounded-full flex items-center justify-center
                        transition-colors duration-200
                        ${hasInput ? 'bg-yellow-500 hover:bg-yellow-400' : 'bg-yellow-700'}
                        disabled:bg-gray-600 disabled:cursor-not-allowed`}
            >
              <FaArrowUp className={hasInput ? 'text-white' : 'text-gray-400'} size={20} />
            </button>
          </form>
        </div>

        {/* ... (rest of the component, with results table modification) */}
        <div className="flex items-center justify-center space-x-3 h-16">
          {isLoading ? (
            <div className="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <>
              {/* Show EITHER suggestions (if no results) OR the reset button (if there are results) */}
              {lastSuccessfulResult === null ? (
                ['General', 'Pitchers', 'Hitters', 'Defense'].map((label) => (
                  <button key={label} className="px-5 py-2 rounded-full text-sm text-white 
                  bg-[rgba(55,65,81,0.57)] border border-[rgba(209,213,219,0.28)] 
                  hover:bg-[rgba(75,85,99,0.7)] backdrop-blur-sm transition-colors">
                      {label}
                  </button>
                ))
              ) : (
                <button 
                  onClick={handleReset} 
                  className="px-5 py-2 rounded-full text-sm text-white 
                             bg-red-600/70 border border-red-400/50 
                             hover:bg-red-500/70 backdrop-blur-sm transition-colors"
                >
                  Clear Results & Start New Query
                </button>
              )}
            </>
          )}
        </div>
        
        <div className="w-full mt-12 space-y-6">
            {error && <div className="p-4 bg-red-900/70 border border-red-700 rounded-lg text-red-200 backdrop-blur-sm">{error}</div>}
            
            {/* Use lastSuccessfulResult to keep the table visible */}
            {lastSuccessfulResult && (
              <div className="p-6 bg-[rgba(31,41,55,0.6)] border border-[rgba(209,213,219,0.28)] rounded-xl backdrop-blur-md space-y-6">
                <div>
                  <h2 className="text-xl font-semibold text-white mb-2">Generated SQL</h2>
                  <pre className="p-4 bg-gray-900/50 border border-gray-600 rounded-lg text-green-300 overflow-x-auto">
                    <code>{lastSuccessfulResult.sql_query}</code>
                  </pre>
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-white mb-2">Results</h2>
                  {lastSuccessfulResult.results.length > 0 ? (
                    <div className="overflow-x-auto">
                        {/* MODIFICATION: Conditional Rendering of Chart or Table */}
                        {visualizationType === 'barchart' ? (
                            <SimpleBarChart results={lastSuccessfulResult.results} />
                        ) : (
                            <table className="min-w-full divide-y divide-gray-600">
                                <thead className="bg-gray-800/50">
                                <tr>
                                    {Object.keys(lastSuccessfulResult.results[0]).map(key => (
                                    <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                                        <button onClick={() => handleSort(key)} className="flex items-center space-x-1 hover:text-white">
                                        <span>{key}</span>
                                        {sortConfig?.key === key && (
                                            <span>{sortConfig.direction === 'ascending' ? '▲' : '▼'}</span>
                                        )}
                                        </button>
                                    </th>
                                    ))}
                                </tr>
                                </thead>
                                <tbody className="bg-gray-900/50 divide-y divide-gray-700">
                                {sortedResults.map((row, i) => (
                                    <tr key={i} className="hover:bg-gray-800/60">
                                    {Object.values(row).map((value, j) => (
                                        <td key={j} className="px-6 py-4 whitespace-nowrap text-sm text-gray-200">{value === null ? 'N/A' : String(value)}</td>
                                    ))}
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                  ) : (
                    <p className="p-4 bg-gray-800/50 border border-gray-600 rounded-lg text-gray-400">The query ran successfully but returned no results.</p>
                  )}
                </div>
              </div>
            )}
        </div>
      </div>
    </main>
  );
}