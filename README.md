# ระบบจัดการทรัพย์สินของรัฐ | Government Asset Management System

ระบบจัดการทรัพย์สินของรัฐบาลไทย สำหรับการติดตาม บันทึก และจัดการทรัพย์สินภาครัฐอย่างมีประสิทธิภาพ

## คุณสมบัติหลัก | Key Features

- **การจัดการทรัพย์สิน** - ลงทะเบียน ติดตาม และจัดการทรัพย์สินทั้งหมด
- **การจัดการโครงการ** - เชื่อมโยงทรัพย์สินกับโครงการต่างๆ
- **การจัดการสถานที่** - จัดการตำแหน่งและสถานที่เก็บทรัพย์สิน
- **ระบบ RBAC** - การควบคุมการเข้าถึงตามบทบาทและสิทธิ์
- **บันทึกการตรวจสอบ** - ติดตามการเปลี่ยนแปลงทั้งหมดในระบบ
- **รายงานและการค้นหา** - ค้นหาและสร้างรายงานขั้นสูง
- **รองรับภาษาไทย** - อินเทอร์เฟซเป็นภาษาไทยเป็นหลัก

## เทคโนโลยีที่ใช้ | Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI components
- **next-intl** - Internationalization (Thai/English)

### Backend
- **NestJS** - Progressive Node.js framework
- **Prisma** - Type-safe database ORM
- **PostgreSQL** - Relational database
- **Redis** - Cache and session store
- **JWT** - Authentication tokens

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Local development
- **Kubernetes** - Production orchestration
- **GitHub Actions** - CI/CD pipeline

## การติดตั้งและพัฒนา | Development Setup

### ความต้องการของระบบ | Prerequisites

- Node.js 18+ 
- pnpm 8+
- Docker และ Docker Compose
- PostgreSQL 15+ (หรือใช้ Docker)

### การติดตั้ง | Installation

1. **โคลนโปรเจค**
```bash
git clone <repository-url>
cd government-asset-management
```

2. **ติดตั้ง dependencies**
```bash
pnpm install
```

3. **ตั้งค่าสิ่งแวดล้อม**
```bash
cp .env.example .env
# แก้ไขค่าต่างๆ ใน .env ตามความเหมาะสม
```

4. **รันฐานข้อมูลด้วย Docker**
```bash
docker compose -f infra/docker-compose.yml up postgres redis -d
```

5. **ตั้งค่าฐานข้อมูล**
```bash
pnpm --filter @government-asset/api run db:generate
pnpm --filter @government-asset/api run db:migrate
pnpm --filter @government-asset/api run db:seed
```

6. **เริ่มการพัฒนา**
```bash
pnpm dev
```

เว็บไซต์จะเปิดที่: http://localhost:3000
API จะเปิดที่: http://localhost:4000
API Documentation: http://localhost:4000/api

### การใช้ Docker Compose

สำหรับการพัฒนาแบบครบวงจร:

```bash
# รันทั้งระบบ
docker compose -f infra/docker-compose.yml up

# รันเฉพาะฐานข้อมูล
docker compose -f infra/docker-compose.yml up postgres redis -d

# หยุดการทำงาน
docker compose -f infra/docker-compose.yml down
```

## การ Deploy แบบ On-premises

### Docker Compose (Production)

```bash
# สร้าง images
docker compose -f infra/docker-compose.yml build

# รันในโหมด production
NODE_ENV=production docker compose -f infra/docker-compose.yml up -d
```

### Kubernetes

1. **ตั้งค่า namespace**
```bash
kubectl apply -f infra/k8s/database.yaml
```

2. **Deploy applications**
```bash
kubectl apply -f infra/k8s/api.yaml
kubectl apply -f infra/k8s/web.yaml
```

3. **ตรวจสอบสถานะ**
```bash
kubectl get pods -n government-asset-management
kubectl get services -n government-asset-management
```

## การจัดการ Secrets (Security)

ระบบนี้ออกแบบให้ปลอดภัยสำหรับการ deploy บน on-premises:

### สำหรับ Development
- ใช้ `.env` file สำหรับการพัฒนา
- ไม่ commit secrets จริงลงใน repository

### สำหรับ Production
ควรใช้ระบบจัดการ secrets เช่น:

- **HashiCorp Vault**
```yaml
# ตัวอย่างการอ้างอิง Vault ใน Kubernetes
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: vault-secrets
        key: DATABASE_URL
```

- **Kubernetes Secrets**
```bash
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL=postgresql://... \
  --from-literal=AUTH_SECRET=...
```

## คำสั่งที่สำคัญ | Important Commands

```bash
# พัฒนา
pnpm dev                    # รันทั้งระบบในโหมดพัฒนา
pnpm build                  # build ทั้งระบบ
pnpm lint                   # ตรวจสอบ code style
pnpm test                   # รัน tests

# ฐานข้อมูล
pnpm db:migrate             # รัน database migrations
pnpm db:generate            # สร้าง Prisma client
pnpm db:seed                # เพิ่มข้อมูลตัวอย่าง

# Docker
pnpm docker:build           # build Docker images
pnpm docker:up              # รัน Docker Compose
pnpm docker:down            # หยุด Docker Compose
```

## โครงสร้างโปรเจค | Project Structure

```
├── apps/
│   ├── web/                # Next.js frontend
│   └── api/                # NestJS backend
├── packages/
│   ├── ui/                 # Shared UI components
│   └── config/             # Shared configuration
├── infra/
│   ├── docker-compose.yml  # Docker Compose setup
│   └── k8s/                # Kubernetes manifests
├── .github/
│   └── workflows/          # CI/CD workflows
└── docs/                   # Documentation
```

## การจัดการข้อมูลหลัก | Master Data

ระบบรองรับข้อมูลหลัก เช่น:
- รายชื่อจังหวัด อำเภอ ตำบล
- ประเภททรัพย์สิน
- สถานะทรัพย์สิน
- หน่วยงานราชการ

สามารถนำเข้าข้อมูลเหล่านี้ผ่าน seed scripts หรือ API endpoints

## การมีส่วนร่วม | Contributing

โปรดอ่าน [CONTRIBUTING.md](CONTRIBUTING.md) สำหรับแนวทางการพัฒนาและ code standards

## ความปลอดภัย | Security

โปรดอ่าน [SECURITY.md](SECURITY.md) สำหรับนีติกรรมความปลอดภัยและการรายงานช่องโหว่

## License

Apache License 2.0 - ดูรายละเอียดใน [LICENSE](LICENSE)

## ติดต่อ | Contact

สำหรับคำถามหรือการสนับสนุน กรุณาติดต่อผ่าน GitHub Issues

---

**หมายเหตุ**: นี่คือ MVP (Minimum Viable Product) สำหรับระบบจัดการทรัพย์สินของรัฐ ระบบจะได้รับการพัฒนาเพิ่มเติมในอนาคต