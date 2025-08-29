import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { PrismaService } from '../prisma/prisma.service';
import { LoginDto } from './dto/auth.dto';
import * as bcrypt from 'bcrypt';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async login(loginDto: LoginDto) {
    // For MVP, return mock JWT token
    // TODO: Implement actual user validation
    const { email, password } = loginDto;

    // Mock validation - replace with actual user lookup
    if (email === 'admin@example.com' && password === 'password123') {
      const payload = {
        sub: '1',
        email: email,
        roles: [{ name: 'admin', permissions: [] }],
      };

      const accessToken = this.jwtService.sign(payload, { expiresIn: '15m' });
      const refreshToken = this.jwtService.sign(payload, { expiresIn: '7d' });

      return {
        access_token: accessToken,
        refresh_token: refreshToken,
        token_type: 'Bearer',
        expires_in: 900, // 15 minutes
      };
    }

    throw new UnauthorizedException('Invalid credentials');
  }

  async logout() {
    // Mock logout - in production, invalidate tokens
    return {
      message: 'Successfully logged out',
    };
  }

  async refreshToken(refreshToken: string) {
    try {
      const payload = this.jwtService.verify(refreshToken);
      const newAccessToken = this.jwtService.sign(
        { sub: payload.sub, email: payload.email, roles: payload.roles },
        { expiresIn: '15m' },
      );

      return {
        access_token: newAccessToken,
        token_type: 'Bearer',
        expires_in: 900,
      };
    } catch (error) {
      throw new UnauthorizedException('Invalid refresh token');
    }
  }

  async validateUser(email: string, password: string) {
    // TODO: Implement actual user validation with Prisma
    const user = await this.prisma.user.findUnique({
      where: { email },
      include: {
        userRoles: {
          include: {
            role: {
              include: {
                permissions: {
                  include: {
                    permission: true,
                  },
                },
              },
            },
          },
        },
      },
    });

    if (user && await bcrypt.compare(password, user.password)) {
      const { password, ...result } = user;
      return result;
    }
    return null;
  }
}