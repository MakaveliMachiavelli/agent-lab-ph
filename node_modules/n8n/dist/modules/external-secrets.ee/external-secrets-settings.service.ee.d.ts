import { SettingsRepository } from '@n8n/db';
import { RoleService } from '../../services/role.service';
export declare class ExternalSecretsSettingsService {
    private readonly settingsRepository;
    private readonly roleService;
    constructor(settingsRepository: SettingsRepository, roleService: RoleService);
    setSystemRolesEnabled(enabled: boolean): Promise<void>;
    isSystemRolesEnabled(): Promise<boolean>;
}
