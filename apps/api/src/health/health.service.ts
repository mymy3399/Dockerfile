import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class HealthService {
  constructor(private prisma: PrismaService) {}

  async getHealthStatus() {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
    };
  }

  async getDetailedHealthStatus() {
    const checks = {
      api: { status: 'ok' },
      database: { status: 'unknown' },
      memory: this.getMemoryUsage(),
    };

    // Check database connection
    try {
      await this.prisma.$queryRaw`SELECT 1`;
      checks.database.status = 'ok';
    } catch (error) {
      checks.database.status = 'error';
      checks.database.error = error.message;
    }

    const overallStatus = Object.values(checks).every(
      (check) => check.status === 'ok',
    )
      ? 'ok'
      : 'error';

    return {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      checks,
    };
  }

  private getMemoryUsage() {
    const used = process.memoryUsage();
    return {
      status: 'ok',
      rss: Math.round((used.rss / 1024 / 1024) * 100) / 100 + ' MB',
      heapTotal: Math.round((used.heapTotal / 1024 / 1024) * 100) / 100 + ' MB',
      heapUsed: Math.round((used.heapUsed / 1024 / 1024) * 100) / 100 + ' MB',
      external: Math.round((used.external / 1024 / 1024) * 100) / 100 + ' MB',
    };
  }
}