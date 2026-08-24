import { ResponseError } from './abstract/response.error';
export declare class ScopeForbiddenError extends ResponseError {
    readonly meta: {
        errorCode: string;
        requiredScope: string;
    };
    constructor(message: string, meta: {
        errorCode: string;
        requiredScope: string;
    }, hint?: string);
}
