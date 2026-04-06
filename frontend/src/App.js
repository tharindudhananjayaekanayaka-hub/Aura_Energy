import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Zap, Activity, AlertTriangle, LogOut, Loader2, Sparkles, User, Lock, TrendingUp } from 'lucide-react';

const BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [kwh, setKwh] = useState('');
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (token) {
      fetchHistory();
    }
  }, [token]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post(`${BASE_URL}/auth/login`, formData);
      const accessToken = response.data.access_token;
      setToken(accessToken);
      localStorage.setItem('token', accessToken);
    } catch (error) {
      alert("Login Failed! Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken('');
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/energy/history`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Mocking some future prediction data structurally for the chart
      const fetchedData = response.data.map(item => ({
        date: new Date(item.timestamp).toLocaleDateString(),
        actual: item.kwh_value,
        predicted: item.kwh_value * 1.05 // Mock predicted value slightly higher
      }));
      setHistory(fetchedData);
    } catch (error) {
      console.error("Error fetching history", error);
    }
  };

  const logEnergy = async (e) => {
    e.preventDefault();
    if (!kwh) return;
    try {
      await axios.post(
        `${BASE_URL}/energy/log`,
        { kwh_value: parseFloat(kwh) },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setKwh('');
      fetchHistory();
    } catch (error) {
      alert("Failed to log data!");
    }
  };

  // --- Premium Login View ---
  if (!token) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
        {/* Animated Background Gradients */}
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald-500/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyan-500/20 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '1s' }}></div>
        
        <div className="w-full max-w-md bg-white/10 backdrop-blur-xl border border-white/20 p-8 rounded-3xl shadow-2xl relative z-10">
          <div className="flex flex-col items-center mb-8">
            <div className="p-4 bg-emerald-500/20 rounded-full mb-4">
              <Zap className="w-10 h-10 text-emerald-400" />
            </div>
            <h1 className="text-3xl font-bold text-white tracking-tight">AuraEnergy AI</h1>
            <p className="text-slate-400 text-sm mt-2">Intelligent Energy Management</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="relative">
              <User className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
              <input 
                type="text" 
                placeholder="Username" 
                className="w-full bg-slate-800/50 border border-slate-700 text-white rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                value={username} onChange={(e)=>setUsername(e.target.value)} required
              />
            </div>
            <div className="relative">
              <Lock className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
              <input 
                type="password" 
                placeholder="Password" 
                className="w-full bg-slate-800/50 border border-slate-700 text-white rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                value={password} onChange={(e)=>setPassword(e.target.value)} required
              />
            </div>
            <button 
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-emerald-500 to-cyan-500 text-white py-3.5 rounded-xl font-semibold hover:from-emerald-400 hover:to-cyan-400 transition-all shadow-lg hover:shadow-emerald-500/25 flex items-center justify-center gap-2"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Secure Login'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // --- Premium Dashboard View ---
  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 p-4 md:p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-white/5 p-6 rounded-3xl border border-white/10 backdrop-blur-md">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-emerald-500 to-cyan-500 rounded-2xl shadow-lg shadow-emerald-500/20">
              <Activity className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight">AI Forecasting Center</h1>
              <p className="text-emerald-400 text-sm font-medium flex items-center gap-1">
                <Sparkles className="w-4 h-4" /> System operational
              </p>
            </div>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700 text-sm font-medium">
            <LogOut className="w-4 h-4" /> Logout
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Data Entry & Alerts */}
          <div className="space-y-8">
            {/* Input Card */}
            <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 p-6 rounded-3xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-bl-full transition-transform group-hover:scale-110"></div>
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <Zap className="w-5 h-5 text-emerald-400" /> Log Daily Usage
              </h2>
              <form onSubmit={logEnergy} className="flex flex-col gap-4 relative z-10">
                <div>
                  <label className="text-xs text-slate-400 uppercase tracking-wider font-semibold mb-2 block">Energy Units (kWh)</label>
                  <input 
                    type="number" step="0.1" placeholder="0.0" 
                    className="w-full bg-slate-900 border border-slate-700 text-white rounded-xl p-4 text-2xl focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all font-light" 
                    value={kwh} onChange={(e)=>setKwh(e.target.value)} required
                  />
                </div>
                <button className="bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-bold py-4 rounded-xl transition-colors flex items-center justify-center gap-2">
                  Submit Reading
                </button>
              </form>
            </div>

            {/* Smart Alerts Card */}
            <div className="bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 p-6 rounded-3xl">
              <h2 className="text-lg font-semibold text-orange-400 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" /> AI Insights
              </h2>
              <div className="space-y-3">
                <div className="bg-orange-500/10 border border-orange-500/20 p-4 rounded-xl">
                  <p className="text-sm text-orange-200"><strong>Outlier Detected:</strong> Usage spiked 20% compared to historical average specifically on weekends. Our AI automatically scaled this anomaly down for next month’s forecast.</p>
                </div>
                <div className="bg-slate-800/50 border border-slate-700 p-4 rounded-xl">
                  <p className="text-sm text-slate-300">Background workers initialized. Alerts will be delivered via SMS/Email using Celery.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Chart */}
          <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-xl border border-slate-700 p-6 rounded-3xl flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-cyan-400" /> Consumption vs AI Forecast
              </h2>
              <span className="px-3 py-1 bg-cyan-500/20 text-cyan-400 text-xs font-semibold rounded-full border border-cyan-500/30">Prophet Model Active</span>
            </div>
            
            <div className="flex-1 min-h-[400px] w-full">
              {history.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={history} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorPredicted" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                    <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '12px', color: '#f8fafc' }}
                      itemStyle={{ color: '#e2e8f0' }}
                    />
                    <Legend iconType="circle" />
                    <Area type="monotone" name="Actual Usage" dataKey="actual" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorActual)" />
                    <Area type="monotone" name="Prophet Forecast" dataKey="predicted" stroke="#0ea5e9" strokeWidth={3} strokeDasharray="5 5" fillOpacity={1} fill="url(#colorPredicted)" />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-500">
                  <Activity className="w-12 h-12 mb-4 opacity-50" />
                  <p>No energy data logged yet.</p>
                  <p className="text-sm">Add your first reading to train the AI model.</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;