import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class AuditInterceptor implements NestInterceptor {
  constructor(
    private configService: ConfigService,
    private prisma: PrismaService,
  ) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    if (this.configService.get('AUDIT_ENABLED') !== 'true') {
      return next.handle();
    }

    const request = context.switchToHttp().getRequest();
    const { method, url, user, ip, headers } = request;

    const auditData = {
      actor: user?.id || 'anonymous',
      action: method,
      resource: url,
      metadata: {
        method,
        url,
        userAgent: headers['user-agent'],
        timestamp: new Date().toISOString(),
      },
      ipAddress: ip,
      userAgent: headers['user-agent'],
    };

    // Log to console
    console.log('Audit Log:', JSON.stringify(auditData));

    return next.handle().pipe(
      tap(async (data) => {
        // TODO: Save to database when AUDIT_ENABLED=true
        try {
          if (this.configService.get('AUDIT_ENABLED') === 'true') {
            // await this.prisma.auditLog.create({ data: auditData });
          }
        } catch (error) {
          console.error('Failed to save audit log:', error);
        }
      }),
    );
  }
}