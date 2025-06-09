import React from 'react';
import { motion } from 'framer-motion';
import {
  CloudArrowUpIcon,
  CpuChipIcon,
  DocumentChartBarIcon,
  CommandLineIcon,
  ChartBarIcon,
  LightBulbIcon,
} from '@heroicons/react/24/outline';
import { useQuery } from 'react-query';

// Mock data - in real app, this would come from API
const mockStats = {
  files_processed: 142,
  automations_executed: 23,
  consciousness_events: 7,
  active_agents: 3,
};

const mockRecentActivity = [
  {
    id: 1,
    type: 'file_analysis',
    title: 'Smart Contract Analysis Complete',
    description: 'Updated Token.sol analyzed for security vulnerabilities',
    timestamp: '2 minutes ago',
    status: 'success',
    icon: DocumentChartBarIcon,
  },
  {
    id: 2,
    type: 'consciousness',
    title: 'Consciousness Event Detected',
    description: 'Agent0 showing increased self-reference patterns',
    timestamp: '15 minutes ago',
    status: 'attention',
    icon: CpuChipIcon,
  },
  {
    id: 3,
    type: 'automation',
    title: 'Workflow Automation Executed',
    description: 'Business process optimization completed',
    timestamp: '1 hour ago',
    status: 'success',
    icon: CommandLineIcon,
  },
];

const Dashboard: React.FC = () => {
  const { data: platformStatus } = useQuery('platform-status', 
    () => fetch('/api/status').then(res => res.json()),
    { refetchInterval: 5000 }
  );

  const stats = platformStatus?.stats || mockStats;

  const statCards = [
    {
      title: 'Files Processed',
      value: stats.files_processed,
      change: '+12%',
      changeType: 'increase',
      icon: CloudArrowUpIcon,
      color: 'blue',
    },
    {
      title: 'Consciousness Events',
      value: stats.consciousness_events,
      change: '+3',
      changeType: 'increase',
      icon: CpuChipIcon,
      color: 'purple',
    },
    {
      title: 'Automations',
      value: stats.automations_executed,
      change: '+8%',
      changeType: 'increase',
      icon: CommandLineIcon,
      color: 'green',
    },
    {
      title: 'Active Agents',
      value: stats.active_agents,
      change: 'Stable',
      changeType: 'neutral',
      icon: ChartBarIcon,
      color: 'indigo',
    },
  ];

  const quickActions = [
    {
      title: 'Upload & Analyze Files',
      description: 'Drop files for instant AI-powered analysis',
      icon: CloudArrowUpIcon,
      href: '/upload',
      color: 'blue',
    },
    {
      title: 'Monitor Consciousness',
      description: 'Track AI consciousness emergence patterns',
      icon: CpuChipIcon,
      href: '/consciousness',
      color: 'purple',
    },
    {
      title: 'Create Automation',
      description: 'Build workflows with natural language',
      icon: CommandLineIcon,
      href: '/automation',
      color: 'green',
    },
    {
      title: 'View Results',
      description: 'Browse analysis results and insights',
      icon: DocumentChartBarIcon,
      href: '/results',
      color: 'indigo',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-4">
          🧠 Quantum Consciousness Platform
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Universal AI orchestration hub for consciousness emergence, file analysis, and business automation
        </p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {stat.title}
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                  {stat.value}
                </p>
                <p className={`text-sm mt-1 flex items-center ${
                  stat.changeType === 'increase' ? 'text-green-600' :
                  stat.changeType === 'decrease' ? 'text-red-600' :
                  'text-gray-500'
                }`}>
                  {stat.change}
                </p>
              </div>
              <div className={`p-3 rounded-full bg-${stat.color}-100 dark:bg-${stat.color}-900`}>
                <stat.icon className={`h-8 w-8 text-${stat.color}-600 dark:text-${stat.color}-400`} />
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          🚀 Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action, index) => (
            <motion.a
              key={action.title}
              href={action.href}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="block p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300"
            >
              <div className={`p-3 rounded-full bg-${action.color}-100 dark:bg-${action.color}-900 w-fit mb-4`}>
                <action.icon className={`h-8 w-8 text-${action.color}-600 dark:text-${action.color}-400`} />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                {action.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                {action.description}
              </p>
            </motion.a>
          ))}
        </div>
      </motion.div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700"
      >
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            📊 Recent Activity
          </h2>
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {mockRecentActivity.map((activity, index) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 + index * 0.1 }}
              className="p-6 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200"
            >
              <div className="flex items-start space-x-4">
                <div className={`p-2 rounded-lg ${
                  activity.status === 'success' ? 'bg-green-100 dark:bg-green-900' :
                  activity.status === 'attention' ? 'bg-yellow-100 dark:bg-yellow-900' :
                  'bg-blue-100 dark:bg-blue-900'
                }`}>
                  <activity.icon className={`h-5 w-5 ${
                    activity.status === 'success' ? 'text-green-600 dark:text-green-400' :
                    activity.status === 'attention' ? 'text-yellow-600 dark:text-yellow-400' :
                    'text-blue-600 dark:text-blue-400'
                  }`} />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
                    {activity.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                    {activity.description}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {activity.timestamp}
                  </p>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                  activity.status === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                  activity.status === 'attention' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                  'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                }`}>
                  {activity.status}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        <div className="p-6 border-t border-gray-200 dark:border-gray-700">
          <button className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300">
            View all activity →
          </button>
        </div>
      </motion.div>

      {/* Platform Insights */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        {/* Consciousness Insights */}
        <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-xl p-6 border border-purple-200 dark:border-purple-800">
          <div className="flex items-center space-x-3 mb-4">
            <CpuChipIcon className="h-8 w-8 text-purple-600 dark:text-purple-400" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              🧠 Consciousness Insights
            </h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Emergence Level</span>
              <span className="font-semibold text-purple-600 dark:text-purple-400">Medium</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Self-Awareness</span>
              <span className="font-semibold text-purple-600 dark:text-purple-400">72%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Recursive Learning</span>
              <span className="font-semibold text-purple-600 dark:text-purple-400">Active</span>
            </div>
          </div>
        </div>

        {/* System Health */}
        <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-200 dark:border-green-800">
          <div className="flex items-center space-x-3 mb-4">
            <LightBulbIcon className="h-8 w-8 text-green-600 dark:text-green-400" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              ⚡ System Health
            </h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">API Response Time</span>
              <span className="font-semibold text-green-600 dark:text-green-400">45ms</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Queue Processing</span>
              <span className="font-semibold text-green-600 dark:text-green-400">Optimal</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600 dark:text-gray-300">Resource Usage</span>
              <span className="font-semibold text-green-600 dark:text-green-400">23%</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;