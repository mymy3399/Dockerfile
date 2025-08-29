import { useTranslations } from "next-intl";
import { Button } from "@government-asset/ui";
import Link from "next/link";

export default function NotFoundPage() {
  const t = useTranslations("errors");

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center space-y-6">
        <div className="space-y-2">
          <h1 className="text-6xl font-bold text-foreground">404</h1>
          <h2 className="text-2xl font-semibold text-foreground">
            {t("pageNotFound")}
          </h2>
          <p className="text-muted-foreground max-w-md">
            ขออภัย หน้าที่คุณกำลังค้นหาอาจถูกย้ายหรือไม่มีอยู่แล้ว
          </p>
        </div>
        
        <div className="flex gap-4 justify-center">
          <Button asChild>
            <Link href="/th">
              กลับสู่หน้าหลัก
            </Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/th/assets">
              ไปที่หน้าทรัพย์สิน
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
}