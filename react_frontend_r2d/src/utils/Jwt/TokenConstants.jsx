// JWT related constants are stored here

/**
 * The lifetime of the access token in minutes (10 Minutes).
 */
export const ACCESS_TOKEN_LIFETIME = 10

/**
 * Intended audience for the access token, part of JWT claims
 */

export const ACCESS_TOKEN_AUDIENCE = "React-Frontend-R2D"
/**
 * Issuer of the access token, part of JWT claims
 */

export const ACCESS_TOKEN_ISSUER = "Django-Backend-R2D"
/**
 * The key to store and retrieve the access token in local storage
 */
export const ACCESS_TOKEN_KEY = "r2d_access_token"

/**
 * The lifetime of refresh tokens in minutes (1440, 1 day)
 */
export const REFRESH_TOKEN_LIFETIME = 60 * 24 * 1 

/**
 * The time to wait before user is deemed to be inactive in milliseconds (7 min)
 */
export const IDLE_TIMEOUT_MS = 7 * 60 * 1000

/**
 * The time to wait before user is warned about inactivity in milliseconds  (1 min)
 * */
export const WARNING_TIMEOUT = 1 * 60 * 1000