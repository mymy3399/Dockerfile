import { SetMetadata } from '@nestjs/common';
import { RoleEnum, PermissionEnum } from './rbac.enums';

export const ROLES_KEY = 'roles';
export const PERMISSIONS_KEY = 'permissions';

export const Roles = (...roles: RoleEnum[]) => SetMetadata(ROLES_KEY, roles);

export const Permissions = (...permissions: PermissionEnum[]) => 
  SetMetadata(PERMISSIONS_KEY, permissions);