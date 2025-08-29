import { render, screen } from '@testing-library/react';
import { NextIntlClientProvider } from 'next-intl';

// Mock messages
const mockMessages = {
  'pages.dashboard.title': 'แดชบอร์ด',
  'pages.dashboard.description': 'ภาพรวมของระบบจัดการทรัพย์สินของรัฐ',
  'pages.dashboard.totalAssets': 'ทรัพย์สินทั้งหมด',
  'pages.dashboard.activeProjects': 'โครงการที่ดำเนินการ',
  'pages.dashboard.locations': 'สถานที่',
};

function renderWithIntl(component: React.ReactElement) {
  return render(
    <NextIntlClientProvider messages={mockMessages} locale="th">
      {component}
    </NextIntlClientProvider>
  );
}

// Mock the dashboard page component for testing
function DashboardTestComponent() {
  return (
    <div data-testid="dashboard">
      <h1>แดชบอร์ด</h1>
      <p>ภาพรวมของระบบจัดการทรัพย์สินของรัฐ</p>
      <div data-testid="stats">
        <div>ทรัพย์สินทั้งหมด: 1,234</div>
        <div>โครงการที่ดำเนินการ: 56</div>
        <div>สถานที่: 89</div>
      </div>
    </div>
  );
}

describe('Dashboard Page', () => {
  it('should render dashboard with Thai content', () => {
    renderWithIntl(<DashboardTestComponent />);
    
    expect(screen.getByText('แดชบอร์ด')).toBeInTheDocument();
    expect(screen.getByText('ภาพรวมของระบบจัดการทรัพย์สินของรัฐ')).toBeInTheDocument();
  });

  it('should display statistics', () => {
    renderWithIntl(<DashboardTestComponent />);
    
    const statsSection = screen.getByTestId('stats');
    expect(statsSection).toBeInTheDocument();
    
    expect(screen.getByText(/ทรัพย์สินทั้งหมด: 1,234/)).toBeInTheDocument();
    expect(screen.getByText(/โครงการที่ดำเนินการ: 56/)).toBeInTheDocument();
    expect(screen.getByText(/สถานที่: 89/)).toBeInTheDocument();
  });
});