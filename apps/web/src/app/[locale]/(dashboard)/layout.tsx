import { AppLayout } from "@/components/app-layout";

export default function LocaleLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  return <AppLayout locale={locale}>{children}</AppLayout>;
}