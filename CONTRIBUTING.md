# แนวทางการมีส่วนร่วม | Contributing Guide

ขอบคุณสำหรับความสนใจในการมีส่วนร่วมพัฒนาระบบจัดการทรัพย์สินของรัฐ! เอกสารนี้จะช่วยแนะนำวิธีการมีส่วนร่วมในโปรเจคนี้

## การเริ่มต้น | Getting Started

### ก่อนเริ่มต้น
- อ่าน [README.md](README.md) เพื่อทำความเข้าใจระบบ
- ตั้งค่า development environment ตาม installation guide
- ตรวจสอบ [Issues](../../issues) ที่เปิดอยู่

### การตั้งค่า Development Environment

```bash
# 1. Fork และ clone repository
git clone https://github.com/your-username/government-asset-management.git
cd government-asset-management

# 2. ติดตั้ง dependencies
pnpm install

# 3. ตั้งค่า environment
cp .env.example .env

# 4. ตั้งค่าฐานข้อมูล
docker compose -f infra/docker-compose.yml up postgres redis -d
pnpm --filter @government-asset/api run db:migrate

# 5. รัน development server
pnpm dev
```

## Code Standards และ Guidelines

### TypeScript Standards
- ใช้ TypeScript สำหรับทุกไฟล์ใหม่
- ใช้ strict mode
- เขียน type definitions ที่ชัดเจน
- หลีกเลี่ยงการใช้ `any` type

```typescript
// ✅ ดี
interface User {
  id: string;
  email: string;
  createdAt: Date;
}

// ❌ หลีกเลี่ยง
const user: any = { ... };
```

### React/Next.js Standards
- ใช้ functional components กับ hooks
- ใช้ TypeScript interfaces สำหรับ props
- Implement proper error boundaries
- ใช้ server components เมื่อเป็นไปได้

```tsx
// ✅ ดี
interface Props {
  title: string;
  onSave: (data: FormData) => void;
}

export function AssetForm({ title, onSave }: Props) {
  // Component implementation
}
```

### NestJS Standards
- ใช้ decorators อย่างถูกต้อง
- Implement proper DTOs และ validation
- ใช้ dependency injection
- เขียน tests สำหรับ services และ controllers

```typescript
// ✅ ดี
@Controller('assets')
export class AssetsController {
  constructor(private readonly assetsService: AssetsService) {}

  @Get()
  @Permissions(PermissionEnum.ASSETS_READ)
  async findAll(): Promise<Asset[]> {
    return this.assetsService.findAll();
  }
}
```

### Database Standards
- ใช้ Prisma migrations สำหรับการเปลี่ยนแปลง schema
- เขียน indexes ที่เหมาะสม
- ใช้ proper data types
- Implement soft deletes เมื่อจำเป็น

```sql
-- ✅ ดี - ใส่ index สำหรับ foreign keys
@@index([projectId])
@@index([locationId])
@@unique([assetCode, agencyAssetCode])
```

## การเขียน Commit Messages

ใช้ Conventional Commits format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: คุณสมบัติใหม่
- `fix`: การแก้ไข bug
- `docs`: การเปลี่ยนแปลง documentation
- `style`: การปรับปรุง formatting/style
- `refactor`: การ refactor code
- `test`: การเพิ่มหรือแก้ไข tests
- `chore`: การปรับปรุง build process หรือ auxiliary tools

### ตัวอย่าง
```bash
feat(assets): add asset export functionality

Add CSV and PDF export options for asset listings
- Implement export service with filtering
- Add export buttons to asset list page
- Include Thai language support for reports

Closes #123
```

## Testing Guidelines

### Frontend Testing
- ใช้ Jest และ React Testing Library
- เขียน unit tests สำหรับ utilities และ hooks
- เขียน integration tests สำหรับ components
- เขียน e2e tests สำหรับ critical user journeys

```typescript
// ตัวอย่าง component test
test('should render asset form with initial values', () => {
  render(<AssetForm initialData={mockAssetData} />);
  
  expect(screen.getByDisplayValue(mockAssetData.name)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /บันทึก/ })).toBeInTheDocument();
});
```

### Backend Testing
- ใช้ Jest สำหรับ unit และ integration tests
- เขียน tests สำหรับทุก service methods
- เขียน e2e tests สำหรับ API endpoints
- Mock external dependencies

```typescript
// ตัวอย่าง service test
describe('AssetsService', () => {
  it('should create new asset', async () => {
    const createDto = { name: 'Test Asset', ... };
    const result = await service.create(createDto);
    
    expect(result.name).toBe(createDto.name);
    expect(mockPrisma.asset.create).toHaveBeenCalledWith({
      data: createDto,
    });
  });
});
```

## การส่ง Pull Request

### ก่อนส่ง PR
1. ตรวจสอบให้แน่ใจว่าผ่าน all tests
```bash
pnpm test
pnpm lint
pnpm type-check
pnpm build
```

2. Update documentation ถ้าจำเป็น
3. เพิ่ม changeset ถ้าเปลี่ยนแปลง public API

### PR Template
```markdown
## การเปลี่ยนแปลง | Changes
- คำอธิบายการเปลี่ยนแปลงที่สำคัญ

## ประเภทของ PR | Type of PR
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## การทดสอบ | Testing
- [ ] Unit tests ผ่าน
- [ ] Integration tests ผ่าน
- [ ] Manual testing เสร็จสิ้น

## Screenshots (ถ้ามี)
<!-- แนบ screenshots สำหรับ UI changes -->

## เกี่ยวข้องกับ Issues
Closes #123
```

### Review Process
1. Automated checks จะรันก่อน
2. Code review จาก maintainers
3. การทดสอบใน staging environment
4. Approval และ merge

## Thai Language Support

### UI Text
- ใช้ `next-intl` สำหรับ internationalization
- เพิ่ม keys ใหม่ใน `messages/th.json` และ `messages/en.json`
- ใช้ภาษาไทยเป็นหลัก แต่รองรับภาษาอังกฤษ

```json
// messages/th.json
{
  "pages": {
    "assets": {
      "title": "จัดการทรัพย์สิน",
      "addButton": "เพิ่มทรัพย์สิน"
    }
  }
}
```

### Code Comments
- เขียน comments เป็นภาษาอังกฤษ
- Documentation ในภาษาไทยและอังกฤษ
- Variable และ function names เป็นภาษาอังกฤษ

## Performance Guidelines

### Frontend Performance
- ใช้ React.lazy() สำหรับ code splitting
- Optimize images และ assets
- ใช้ proper caching strategies
- Monitor Core Web Vitals

### Backend Performance
- ใช้ database indexes อย่างเหมาะสม
- Implement caching กับ Redis
- ใช้ pagination สำหรับ large datasets
- Monitor query performance

## Security Guidelines

- อ่าน [SECURITY.md](SECURITY.md) 
- ไม่ commit secrets หรือ sensitive data
- ใช้ proper input validation
- Implement proper error handling
- Follow OWASP security practices

## การได้รับความช่วยเหลือ

### Resources
- [GitHub Issues](../../issues) - สำหรับ bugs และ feature requests
- [GitHub Discussions](../../discussions) - สำหรับคำถามทั่วไป
- Documentation - ใน `/docs` folder

### คำถามที่พบบ่อย

**Q: จะเริ่มพัฒนาคุณสมบัติใหม่ได้อย่างไร?**
A: เช็ค existing issues ก่อน หากไม่มี ให้สร้าง issue ใหม่เพื่อหารือ

**Q: จะรัน tests ได้อย่างไร?**
A: ใช้คำสั่ง `pnpm test` สำหรับทั้งหมด หรือ `pnpm test --filter <package>` สำหรับ specific package

**Q: Database migration ทำงานอย่างไร?**
A: ใช้ `pnpm --filter @government-asset/api run db:migrate` เพื่อรัน migrations

## Code of Conduct

- เคารพและใจดีต่อผู้มีส่วนร่วมทุกคน
- ให้ feedback ที่สร้างสรรค์
- ยินดีรับฟังความคิดเห็นที่แตกต่าง
- ให้ความช่วยเหลือผู้เริ่มต้น

---

ขอบคุณสำหรับการมีส่วนร่วมในการพัฒนาระบบจัดการทรัพย์สินของรัฐ!