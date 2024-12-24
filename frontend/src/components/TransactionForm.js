import React, { useState } from 'react';
import { recordTransaction } from '../services/api';

const TransactionForm = () => {
  const [userId, setUserId] = useState('');
  const [storeId, setStoreId] = useState('');
  const [amountDue, setAmountDue] = useState('');
  const [remainingChange, setRemainingChange] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await recordTransaction({ user_id: userId, store_id: storeId, amount_due: amountDue, remaining_change: remainingChange });
      alert(response.data.message);
    } catch (error) {
      alert('Transaction recording failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Record Transaction</h2>
      <input type="text" placeholder="User ID" value={userId} onChange={(e) => setUserId(e.target.value)} required />
      <input type="text" placeholder="Store ID" value={storeId} onChange={(e) => setStoreId(e.target.value)} required />
      <input type="number" placeholder="Amount Due" value={amountDue} onChange={(e) => setAmountDue(e.target.value)} required />
      <input type="number" placeholder="Remaining Change" value={remainingChange} onChange={(e) => setRemainingChange(e.target.value)} required />
      <button type="submit">Record</button>
    </form>
  );
};

export default TransactionForm;