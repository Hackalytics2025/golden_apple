import React from "react";
import { TableauViz } from "@tableau/tableau-viz";

interface TableauDashboardProps {
  vizUrl: string;
}

const TableauDashboard: React.FC<TableauDashboardProps> = ({ vizUrl }) => {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Market Analysis Dashboard
        </h1>

        <div className="bg-white rounded-lg shadow-lg p-4">
          <TableauViz
            vizUrl={vizUrl}
            height="800px"
            width="100%"
            hideTabs={false}
            hideToolbar={false}
          />
        </div>
      </div>
    </div>
  );
};

export default TableauDashboard;
