"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@government-asset/ui";
import { cn } from "@government-asset/ui";

interface AppLayoutProps {
  children: React.ReactNode;
  locale: string;
}

export function AppLayout({ children, locale }: AppLayoutProps) {
  const t = useTranslations();
  const pathname = usePathname();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const navigation = [
    {
      name: t("nav.dashboard"),
      href: `/${locale}`,
      current: pathname === `/${locale}`,
    },
    {
      name: t("nav.assets"),
      href: `/${locale}/assets`,
      current: pathname === `/${locale}/assets`,
    },
    {
      name: t("nav.projects"),
      href: `/${locale}/projects`,
      current: pathname === `/${locale}/projects`,
    },
    {
      name: t("nav.locations"),
      href: `/${locale}/locations`,
      current: pathname === `/${locale}/locations`,
    },
  ];

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div
        className={cn(
          "flex flex-col bg-card border-r transition-all duration-300",
          isSidebarOpen ? "w-64" : "w-16"
        )}
      >
        <div className="flex items-center h-16 px-4 border-b">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-thai-blue rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">GAM</span>
            </div>
            {isSidebarOpen && (
              <h1 className="text-lg font-semibold text-foreground">
                Asset Management
              </h1>
            )}
          </div>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-2">
          {navigation.map((item) => (
            <Link key={item.name} href={item.href}>
              <div
                className={cn(
                  "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  item.current
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent"
                )}
              >
                <span className={cn(!isSidebarOpen && "sr-only")}>
                  {item.name}
                </span>
              </div>
            </Link>
          ))}
        </nav>

        <div className="border-t p-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="w-full justify-start"
          >
            {isSidebarOpen ? "ย่อ" : "ขยาย"}
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-card border-b px-6 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h2 className="text-xl font-semibold text-foreground">
              {t("nav.dashboard")}
            </h2>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm">
              {locale === "th" ? "EN" : "TH"}
            </Button>
            <Button variant="outline" size="sm">
              {t("nav.logout")}
            </Button>
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
}