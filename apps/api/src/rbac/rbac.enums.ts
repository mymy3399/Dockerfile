export enum RoleEnum {
  SUPER_ADMIN = 'super_admin',
  ADMIN = 'admin',
  ASSET_MANAGER = 'asset_manager',
  PROJECT_MANAGER = 'project_manager',
  LOCATION_MANAGER = 'location_manager',
  AUDITOR = 'auditor',
  VIEWER = 'viewer',
}

export enum PermissionEnum {
  // Asset permissions
  ASSETS_CREATE = 'assets:create',
  ASSETS_READ = 'assets:read',
  ASSETS_UPDATE = 'assets:update',
  ASSETS_DELETE = 'assets:delete',
  ASSETS_EXPORT = 'assets:export',
  ASSETS_IMPORT = 'assets:import',

  // Project permissions
  PROJECTS_CREATE = 'projects:create',
  PROJECTS_READ = 'projects:read',
  PROJECTS_UPDATE = 'projects:update',
  PROJECTS_DELETE = 'projects:delete',

  // Location permissions
  LOCATIONS_CREATE = 'locations:create',
  LOCATIONS_READ = 'locations:read',
  LOCATIONS_UPDATE = 'locations:update',
  LOCATIONS_DELETE = 'locations:delete',

  // User management permissions
  USERS_CREATE = 'users:create',
  USERS_READ = 'users:read',
  USERS_UPDATE = 'users:update',
  USERS_DELETE = 'users:delete',

  // System permissions
  SYSTEM_ADMIN = 'system:admin',
  AUDIT_READ = 'audit:read',
  REPORTS_READ = 'reports:read',
}