import { useState, useEffect } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Tooltip } from "recharts";

function App() {
  const API = "https://spendora-0ude.onrender.com"; // replace if needed

  const theme = {
    bg: "#F7F4D5",
    card: "#ffffff",
    primary: "#839958",
    dark: "#0A3323",
    accent: "#D3968C"
  };

  const COLORS = [
    "#0A3323",
    "#839958",
    "#D3968C",
    "#105666",
    "#A3B18A"
  ];

  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [type, setType] = useState("expense");
  const [transactions, setTransactions] = useState([]);
  const [insight, setInsight] = useState("");

  const fetchData = async () => {
    try {
      const res = await axios.get(`${API}/transactions`);
      setTransactions(res.data);

      const insightRes = await axios.get(`${API}/insights`);
      setInsight(insightRes.data.insight);
    } catch (err) {
      console.error(err);
    }
  };

  const addTransaction = async () => {
    if (!title || !amount) return;

    try {
      await axios.post(`${API}/transactions`, {
        title: title,
        amount: parseFloat(amount),
        type: type
      });

      setTitle("");
      setAmount("");
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const deleteTransaction = async (id) => {
    try {
      await axios.delete(`${API}/transactions/${id}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const resetData = async () => {
    try {
      await axios.delete(`${API}/reset`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const expenseData = transactions
    .filter((t) => t.type === "expense")
    .map((t) => ({
      name: t.title,
      value: t.amount
    }));

  return (
    <div
      style={{
        background: theme.bg,
        minHeight: "100vh",
        padding: "30px",
        fontFamily: "Poppins"
      }}
    >
      <h2 style={{ color: theme.dark }}>Spendora</h2>

      {/* FORM */}
      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          marginBottom: "20px",
          display: "flex",
          gap: "10px"
        }}
      >
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>

        <button onClick={addTransaction} style={{ background: theme.primary }}>
          Add
        </button>
      </div>

      {/* RESET BUTTON */}
      <button
        onClick={resetData}
        style={{
          background: theme.dark,
          color: "white",
          padding: "10px",
          borderRadius: "8px",
          border: "none",
          marginBottom: "20px",
          cursor: "pointer"
        }}
      >
        Reset All Data
      </button>

      {/* INSIGHT */}
      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          marginBottom: "20px"
        }}
      >
        <h4>Insight</h4>
        <p>{insight}</p>
      </div>

      {/* TRANSACTIONS */}
      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px"
        }}
      >
        <h4>Transactions</h4>

        {transactions.length === 0 ? (
          <p>No transactions yet</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {transactions.map((t) => (
              <li
                key={t.id}
                style={{
                  padding: "10px",
                  marginBottom: "8px",
                  background: "#f9f9f9",
                  borderRadius: "8px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center"
                }}
              >
                <span>{t.title}</span>
                <span>₹{t.amount}</span>
                <span>{t.type}</span>

                <button
                  onClick={() => deleteTransaction(t.id)}
                  style={{
                    background: theme.accent,
                    border: "none",
                    color: "white",
                    padding: "6px 10px",
                    borderRadius: "6px",
                    cursor: "pointer"
                  }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* CHART */}
      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          marginTop: "20px"
        }}
      >
        <h4>Expense Breakdown</h4>

        {expenseData.length === 0 ? (
          <p>No expense data</p>
        ) : (
          <PieChart width={300} height={300}>
            <Pie data={expenseData} dataKey="value" nameKey="name" outerRadius={100}>
              {expenseData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        )}
      </div>
    </div>
  );
}

export default App;