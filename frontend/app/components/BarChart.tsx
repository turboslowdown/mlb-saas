"use client";

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import debounce from 'lodash.debounce';

interface ChartData {
  results: Record<string, any>[];
}

const SimpleBarChart = ({ results }: ChartData) => {
  // Get the keys for the X and Y axis from the first data object
  const dataKeys = Object.keys(results[0]);
  const xAxisKey = dataKeys[0];
  const yAxisKey = dataKeys[1];

  // A small hack to force re-render on window resize for responsiveness
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const handleResize = debounce(() => {
        setWidth(window.innerWidth);
    }, 200);
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);


  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={results}
        margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
        <XAxis 
            dataKey={xAxisKey} 
            stroke="#9ca3af"
            tick={{ fill: '#d1d5db', fontSize: 12 }} 
        />
        <YAxis 
            stroke="#9ca3af"
            tick={{ fill: '#d1d5db', fontSize: 12 }} 
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(31, 41, 55, 0.8)',
            borderColor: 'rgba(255, 255, 255, 0.2)',
            color: '#ffffff'
          }}
          cursor={{ fill: 'rgba(255, 255, 255, 0.1)' }}
        />
        <Bar dataKey={yAxisKey} fill="#f59e0b" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default SimpleBarChart;