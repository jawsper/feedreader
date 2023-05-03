/* tslint:disable */
/* eslint-disable */
/**
 * Feedreader
 * Feedreader
 *
 * The version of the OpenAPI document: 1.28.1
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from "../runtime";
/**
 *
 * @export
 * @interface OutlineFeed
 */
export interface OutlineFeed {
  /**
   *
   * @type {number}
   * @memberof OutlineFeed
   */
  readonly id?: number;
  /**
   *
   * @type {string}
   * @memberof OutlineFeed
   */
  title: string;
  /**
   *
   * @type {string}
   * @memberof OutlineFeed
   */
  html_url: string;
  /**
   *
   * @type {boolean}
   * @memberof OutlineFeed
   */
  is_nsfw?: boolean;
  /**
   *
   * @type {string}
   * @memberof OutlineFeed
   */
  readonly icon?: string;
}

/**
 * Check if a given object implements the OutlineFeed interface.
 */
export function instanceOfOutlineFeed(value: object): boolean {
  let isInstance = true;
  isInstance = isInstance && "title" in value;
  isInstance = isInstance && "html_url" in value;

  return isInstance;
}

export function OutlineFeedFromJSON(json: any): OutlineFeed {
  return OutlineFeedFromJSONTyped(json, false);
}

export function OutlineFeedFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): OutlineFeed {
  if (json === undefined || json === null) {
    return json;
  }
  return {
    id: !exists(json, "id") ? undefined : json["id"],
    title: json["title"],
    html_url: json["html_url"],
    is_nsfw: !exists(json, "is_nsfw") ? undefined : json["is_nsfw"],
    icon: !exists(json, "icon") ? undefined : json["icon"],
  };
}

export function OutlineFeedToJSON(value?: OutlineFeed | null): any {
  if (value === undefined) {
    return undefined;
  }
  if (value === null) {
    return null;
  }
  return {
    title: value.title,
    html_url: value.html_url,
    is_nsfw: value.is_nsfw,
  };
}
