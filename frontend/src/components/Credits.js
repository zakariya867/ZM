import React, { useState } from 'react';
import { getUserCredits, getStoreCredits } from '../services/api';

const Credits = () => {
  const [userId, setUserId] = useState('');
  const [storeId, setStoreId] = useState('');
  const [credits, setCredits] = useState(null);

  const handleGetUserCredits = async () => {
    try {
      const response = await getUserCredits(userId);
      setCredits(response.data.total_credits);
    } catch (error) {
      alert('Failed to fetch user credits');
    }
  };

  const handleGetStoreCredits = async () => {
    try {
      const response = await getStoreCredits(storeId);
      setCredits(response.data.total_credits);
    } catch (error) {
      alert('Failed to fetch store credits');
    }
  };

  return (
    <div>
      <h2>View Credits</h2>
      <input type="text" placeholder="User ID" value={userId} onChange={(e) => setUserId(e.target.value)} />
      <button onClick={handleGetUserCredits}>Get User Credits</button>
      <input type="text" placeholder="Store ID" value={storeId} onChange={(e) => setStoreId(e.target.value)} />
      <button onClick={handleGetStoreCredits}>Get Store Credits</button>
      {credits !== null && (
        <div>
          <h3>Total Credits: {credits}</h3>
        </div>
      )}
    </div>
  );
};

export default Credits;