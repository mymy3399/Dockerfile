import { useTranslations } from "next-intl";
import { Button, Card, CardContent, CardHeader, CardTitle, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@government-asset/ui";

export default function AssetsPage() {
  const t = useTranslations("pages.assets");

  // Mock data for demonstration
  const assets = [
    {
      id: 1,
      assetCode: "AST-001",
      name: "เครื่องคอมพิวเตอร์ Desktop",
      category: "IT Equipment",
      status: "ใช้งาน",
      location: "อาคาร A ชั้น 2",
    },
    {
      id: 2,
      assetCode: "AST-002", 
      name: "เครื่องปริ้นเตอร์ Laser",
      category: "Office Equipment",
      status: "ใช้งาน",
      location: "อาคาร B ชั้น 1",
    },
    {
      id: 3,
      assetCode: "AST-003",
      name: "โต๊ะทำงาน",
      category: "Furniture",
      status: "ชำรุด",
      location: "อาคาร A ชั้น 3",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">{t("title")}</h1>
          <p className="text-muted-foreground mt-2">{t("description")}</p>
        </div>
        <Button>{t("addAsset")}</Button>
      </div>

      {/* Search and Filter */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder={t("search")}
                className="w-full px-3 py-2 border rounded-md bg-background"
              />
            </div>
            <Button variant="outline">ค้นหา</Button>
          </div>
        </CardContent>
      </Card>

      {/* Assets Table */}
      <Card>
        <CardHeader>
          <CardTitle>รายการทรัพย์สิน</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t("assetCode")}</TableHead>
                <TableHead>{t("assetName")}</TableHead>
                <TableHead>{t("category")}</TableHead>
                <TableHead>{t("status")}</TableHead>
                <TableHead>{t("location")}</TableHead>
                <TableHead>{t("actions")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {assets.map((asset) => (
                <TableRow key={asset.id}>
                  <TableCell className="font-medium">{asset.assetCode}</TableCell>
                  <TableCell>{asset.name}</TableCell>
                  <TableCell>{asset.category}</TableCell>
                  <TableCell>
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        asset.status === "ใช้งาน"
                          ? "bg-green-100 text-green-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {asset.status}
                    </span>
                  </TableCell>
                  <TableCell>{asset.location}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        ดู
                      </Button>
                      <Button variant="outline" size="sm">
                        แก้ไข
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}