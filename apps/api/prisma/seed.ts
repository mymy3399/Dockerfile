import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting seed...');

  // Create default roles
  const superAdminRole = await prisma.role.upsert({
    where: { name: 'super_admin' },
    update: {},
    create: {
      name: 'super_admin',
      description: 'Super Administrator with full access',
    },
  });

  const adminRole = await prisma.role.upsert({
    where: { name: 'admin' },
    update: {},
    create: {
      name: 'admin',
      description: 'Administrator with management access',
    },
  });

  const viewerRole = await prisma.role.upsert({
    where: { name: 'viewer' },
    update: {},
    create: {
      name: 'viewer',
      description: 'Viewer with read-only access',
    },
  });

  console.log('✅ Created default roles');

  // Create sample permissions
  const permissions = [
    { name: 'assets:create', description: 'Create assets', resource: 'assets', action: 'create' },
    { name: 'assets:read', description: 'Read assets', resource: 'assets', action: 'read' },
    { name: 'assets:update', description: 'Update assets', resource: 'assets', action: 'update' },
    { name: 'assets:delete', description: 'Delete assets', resource: 'assets', action: 'delete' },
    { name: 'projects:create', description: 'Create projects', resource: 'projects', action: 'create' },
    { name: 'projects:read', description: 'Read projects', resource: 'projects', action: 'read' },
    { name: 'locations:create', description: 'Create locations', resource: 'locations', action: 'create' },
    { name: 'locations:read', description: 'Read locations', resource: 'locations', action: 'read' },
  ];

  for (const permission of permissions) {
    await prisma.permission.upsert({
      where: { name: permission.name },
      update: {},
      create: permission,
    });
  }

  console.log('✅ Created sample permissions');

  // Create sample locations
  const mainOffice = await prisma.location.upsert({
    where: { locationCode: 'LOC-001' },
    update: {},
    create: {
      locationCode: 'LOC-001',
      name: 'อาคารสำนักงานหลัก',
      type: 'อาคารสำนักงาน',
      address: '123 ถนนราชดำเนิน แขวงบางรัก เขตบางรัก',
      province: 'กรุงเทพมหานคร',
      district: 'บางรัก',
      subDistrict: 'บางรัก',
      postalCode: '10500',
    },
  });

  const warehouse = await prisma.location.upsert({
    where: { locationCode: 'LOC-002' },
    update: {},
    create: {
      locationCode: 'LOC-002',
      name: 'โกดังเก็บของ',
      type: 'โกดัง',
      address: '456 ถนนสาทร แขวงสีลม เขตบางรัก',
      province: 'กรุงเทพมหานคร',
      district: 'บางรัก',
      subDistrict: 'สีลม',
      postalCode: '10500',
    },
  });

  console.log('✅ Created sample locations');

  // Create sample project
  const project = await prisma.project.upsert({
    where: { projectCode: 'PRJ-001' },
    update: {},
    create: {
      projectCode: 'PRJ-001',
      name: 'โครงการจัดซื้อคอมพิวเตอร์ประจำปี 2024',
      description: 'จัดซื้อคอมพิวเตอร์และอุปกรณ์ IT สำหรับใช้งานในสำนักงาน',
      budget: 2500000,
      status: 'active',
      startDate: new Date('2024-01-01'),
      endDate: new Date('2024-12-31'),
    },
  });

  console.log('✅ Created sample project');

  // Create sample assets
  await prisma.asset.upsert({
    where: { assetCode: 'AST-001' },
    update: {},
    create: {
      assetCode: 'AST-001',
      agencyAssetCode: 'IT-2024-001',
      name: 'เครื่องคอมพิวเตอร์ Desktop Dell OptiPlex 7090',
      description: 'คอมพิวเตอร์ตั้งโต๊ะ CPU Intel Core i5 RAM 8GB HDD 1TB',
      type: 'คอมพิวเตอร์',
      category: 'IT Equipment',
      brand: 'Dell',
      model: 'OptiPlex 7090',
      unitPrice: 25000,
      quantity: 1,
      unit: 'เครื่อง',
      status: 'active',
      condition: 'ดี',
      procuredAt: new Date('2024-01-15'),
      inServiceAt: new Date('2024-01-20'),
      warrantyEndAt: new Date('2027-01-15'),
      projectId: project.id,
      locationId: mainOffice.id,
    },
  });

  await prisma.asset.upsert({
    where: { assetCode: 'AST-002' },
    update: {},
    create: {
      assetCode: 'AST-002',
      agencyAssetCode: 'IT-2024-002',
      name: 'เครื่องปริ้นเตอร์ HP LaserJet Pro M404dn',
      description: 'เครื่องพิมพ์เลเซอร์ขาวดำ ความเร็วพิมพ์ 38 หน้า/นาที',
      type: 'เครื่องปริ้นเตอร์',
      category: 'Office Equipment',
      brand: 'HP',
      model: 'LaserJet Pro M404dn',
      unitPrice: 8500,
      quantity: 1,
      unit: 'เครื่อง',
      status: 'active',
      condition: 'ดี',
      procuredAt: new Date('2024-02-01'),
      inServiceAt: new Date('2024-02-05'),
      warrantyEndAt: new Date('2027-02-01'),
      projectId: project.id,
      locationId: mainOffice.id,
    },
  });

  console.log('✅ Created sample assets');

  // Create sample tags
  const itTag = await prisma.tag.upsert({
    where: { name: 'IT Equipment' },
    update: {},
    create: {
      name: 'IT Equipment',
      color: '#3B82F6',
      description: 'อุปกรณ์เทคโนโลยีสารสนเทศ',
    },
  });

  const officeTag = await prisma.tag.upsert({
    where: { name: 'Office Equipment' },
    update: {},
    create: {
      name: 'Office Equipment',
      color: '#10B981',
      description: 'อุปกรณ์สำนักงาน',
    },
  });

  console.log('✅ Created sample tags');

  console.log('🎉 Seed completed successfully!');
  
  console.log('\n📊 Summary:');
  console.log(`- Roles: ${await prisma.role.count()}`);
  console.log(`- Permissions: ${await prisma.permission.count()}`);
  console.log(`- Locations: ${await prisma.location.count()}`);
  console.log(`- Projects: ${await prisma.project.count()}`);
  console.log(`- Assets: ${await prisma.asset.count()}`);
  console.log(`- Tags: ${await prisma.tag.count()}`);
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error('❌ Seed failed:', e);
    await prisma.$disconnect();
    process.exit(1);
  });