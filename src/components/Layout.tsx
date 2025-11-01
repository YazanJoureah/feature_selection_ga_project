import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card';

const SidebarLink: React.FC<{ to: string; children: React.ReactNode }> = ({ to, children }) => {
  return (
    <NavLink to={to} className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
      <Button asChild variant="ghost" className="nav-button">
        <span className="nav-button-content">{children}</span>
      </Button>
    </NavLink>
  );
};

const Layout: React.FC = () => {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="logo">FS</div>

        <nav className="nav">
          <SidebarLink to="/">Home</SidebarLink>
          <SidebarLink to="/upload">Upload</SidebarLink>
          <SidebarLink to="/compare">Compare</SidebarLink>
          <SidebarLink to="/results">Results</SidebarLink>
          <SidebarLink to="/about">About</SidebarLink>
        </nav>

        <div className="sidebar-footer">v1.0</div>
      </aside>

      <main className="main-content">
        <div className="content-wrap">
          <Card>
            <div className="content-inner">
              <Outlet />
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Layout;
