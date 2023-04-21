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
 * @interface NewFeed
 */
export interface NewFeed {
  /**
   *
   * @type {string}
   * @memberof NewFeed
   */
  xml_url: string;
}

/**
 * Check if a given object implements the NewFeed interface.
 */
export function instanceOfNewFeed(value: object): boolean {
  let isInstance = true;
  isInstance = isInstance && "xml_url" in value;

  return isInstance;
}

export function NewFeedFromJSON(json: any): NewFeed {
  return NewFeedFromJSONTyped(json, false);
}

export function NewFeedFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): NewFeed {
  if (json === undefined || json === null) {
    return json;
  }
  return {
    xml_url: json["xml_url"],
  };
}

export function NewFeedToJSON(value?: NewFeed | null): any {
  if (value === undefined) {
    return undefined;
  }
  if (value === null) {
    return null;
  }
  return {
    xml_url: value.xml_url,
  };
}