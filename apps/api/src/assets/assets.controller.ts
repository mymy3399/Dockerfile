import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { ApiTags, ApiResponse } from '@nestjs/swagger';
import { AssetsService } from './assets.service';
import { Permissions } from '../rbac/rbac.decorators';
import { PermissionEnum } from '../rbac/rbac.enums';

@ApiTags('Assets')
@Controller('assets')
export class AssetsController {
  constructor(private readonly assetsService: AssetsService) {}

  @Get()
  @Permissions(PermissionEnum.ASSETS_READ)
  @ApiResponse({ status: 200, description: 'List all assets' })
  async findAll() {
    return this.assetsService.findAll();
  }

  @Get(':id')
  @Permissions(PermissionEnum.ASSETS_READ)
  @ApiResponse({ status: 200, description: 'Get asset by ID' })
  async findOne(@Param('id') id: string) {
    return this.assetsService.findOne(id);
  }

  @Post()
  @Permissions(PermissionEnum.ASSETS_CREATE)
  @ApiResponse({ status: 201, description: 'Create new asset' })
  async create(@Body() createAssetDto: any) {
    return this.assetsService.create(createAssetDto);
  }

  @Put(':id')
  @Permissions(PermissionEnum.ASSETS_UPDATE)
  @ApiResponse({ status: 200, description: 'Update asset' })
  async update(@Param('id') id: string, @Body() updateAssetDto: any) {
    return this.assetsService.update(id, updateAssetDto);
  }

  @Delete(':id')
  @Permissions(PermissionEnum.ASSETS_DELETE)
  @ApiResponse({ status: 200, description: 'Delete asset' })
  async remove(@Param('id') id: string) {
    return this.assetsService.remove(id);
  }
}