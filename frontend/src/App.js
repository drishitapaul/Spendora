import { useState, useEffect } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Tooltip } from "recharts";

function App() {
  const API = "https://spendora-0ude.onrender.com";

  const theme = {
    bg: "#F7F4D5",
    card: "#ffffff",
    primary: "#839958",
    dark: "#0A3323",
    accent: "#D3968C",
    deep: "#105666"
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

  // eslint-disable-next-line react-hooks/exhaustive-deps
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
      <h2 style={{ color: theme.dark }}>Lofi Finance</h2>

      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          marginBottom: "20px",
          display: "flex",
          gap: "10px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.05)"
        }}
      >
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ddd"
          }}
        />

        <input
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ddd"
          }}
        />

        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "8px"
          }}
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>

        <button
          onClick={addTransaction}
          style={{
            background: theme.primary,
            color: "white",
            border: "none",
            padding: "10px 16px",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Add
        </button>
      </div>

      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          marginBottom: "20px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.05)"
        }}
      >
        <h4>Insight</h4>
        <p>{insight}</p>
      </div>

      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.05)"
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
                  justifyContent: "space-between"
                }}
              >
                <span>{t.title}</span>
                <span>₹{t.amount}</span>
                <span>{t.type}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div
        style={{
          background: theme.card,
          padding: "20px",
          borderRadius: "16px",
          marginTop: "20px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.05)"
        }}
      >
        <h4>Expense Breakdown</h4>

        {expenseData.length === 0 ? (
          <p>No expense data available</p>
        ) : (
          <PieChart width={300} height={300}>
            <Pie
              data={expenseData}
              dataKey="value"
              nameKey="name"
              outerRadius={100}
            >
              {expenseData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
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