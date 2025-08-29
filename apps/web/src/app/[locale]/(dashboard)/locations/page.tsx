import { useTranslations } from "next-intl";
import { Button, Card, CardContent, CardHeader, CardTitle, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@government-asset/ui";

export default function LocationsPage() {
  const t = useTranslations("pages.locations");

  // Mock data
  const locations = [
    {
      id: 1,
      locationCode: "LOC-001",
      name: "อาคารสำนักงานหลัก",
      type: "อาคารสำนักงาน",
      province: "กรุงเทพมหานคร",
      district: "บางรัก",
    },
    {
      id: 2,
      locationCode: "LOC-002",
      name: "โกดังเก็บของ",
      type: "โกดัง",
      province: "กรุงเทพมหานคร", 
      district: "สาทร",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">{t("title")}</h1>
          <p className="text-muted-foreground mt-2">{t("description")}</p>
        </div>
        <Button>{t("addLocation")}</Button>
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

      {/* Locations Table */}
      <Card>
        <CardHeader>
          <CardTitle>รายการสถานที่</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t("locationCode")}</TableHead>
                <TableHead>{t("locationName")}</TableHead>
                <TableHead>{t("type")}</TableHead>
                <TableHead>{t("province")}</TableHead>
                <TableHead>{t("district")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {locations.map((location) => (
                <TableRow key={location.id}>
                  <TableCell className="font-medium">{location.locationCode}</TableCell>
                  <TableCell>{location.name}</TableCell>
                  <TableCell>{location.type}</TableCell>
                  <TableCell>{location.province}</TableCell>
                  <TableCell>{location.district}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}