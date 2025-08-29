import { useTranslations } from "next-intl";
import { Button, Card, CardContent, CardHeader, CardTitle, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@government-asset/ui";

export default function ProjectsPage() {
  const t = useTranslations("pages.projects");

  // Mock data
  const projects = [
    {
      id: 1,
      projectCode: "PRJ-001",
      name: "โครงการจัดซื้อคอมพิวเตอร์",
      status: "ดำเนินการ",
      budget: "2,500,000",
      startDate: "2024-01-01",
      endDate: "2024-06-30",
    },
    {
      id: 2,
      projectCode: "PRJ-002",
      name: "โครงการปรับปรุงสำนักงาน",
      status: "เสร็จสิ้น",
      budget: "1,800,000",
      startDate: "2023-09-01",
      endDate: "2023-12-31",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">{t("title")}</h1>
          <p className="text-muted-foreground mt-2">{t("description")}</p>
        </div>
        <Button>{t("addProject")}</Button>
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

      {/* Projects Table */}
      <Card>
        <CardHeader>
          <CardTitle>รายการโครงการ</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t("projectCode")}</TableHead>
                <TableHead>{t("projectName")}</TableHead>
                <TableHead>{t("status")}</TableHead>
                <TableHead>{t("budget")}</TableHead>
                <TableHead>{t("startDate")}</TableHead>
                <TableHead>{t("endDate")}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {projects.map((project) => (
                <TableRow key={project.id}>
                  <TableCell className="font-medium">{project.projectCode}</TableCell>
                  <TableCell>{project.name}</TableCell>
                  <TableCell>
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${
                        project.status === "ดำเนินการ"
                          ? "bg-blue-100 text-blue-800"
                          : "bg-green-100 text-green-800"
                      }`}
                    >
                      {project.status}
                    </span>
                  </TableCell>
                  <TableCell>{project.budget} บาท</TableCell>
                  <TableCell>{project.startDate}</TableCell>
                  <TableCell>{project.endDate}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}