/* tslint:disable */
/* eslint-disable */
/**
 * Feedreader
 * Feedreader
 *
 * The version of the OpenAPI document: 2.0.14
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
 * @interface Post
 */
export interface Post {
  /**
   *
   * @type {number}
   * @memberof Post
   */
  readonly id?: number;
  /**
   *
   * @type {string}
   * @memberof Post
   */
  readonly link?: string;
  /**
   *
   * @type {string}
   * @memberof Post
   */
  readonly author?: string;
  /**
   *
   * @type {string}
   * @memberof Post
   */
  readonly title?: string;
  /**
   *
   * @type {string}
   * @memberof Post
   */
  readonly feed_title?: string;
  /**
   *
   * @type {Date}
   * @memberof Post
   */
  readonly pub_date?: Date;
  /**
   *
   * @type {string}
   * @memberof Post
   */
  readonly content?: string;
  /**
   *
   * @type {boolean}
   * @memberof Post
   */
  starred?: boolean;
  /**
   *
   * @type {boolean}
   * @memberof Post
   */
  read?: boolean;
}

/**
 * Check if a given object implements the Post interface.
 */
export function instanceOfPost(value: object): boolean {
  let isInstance = true;

  return isInstance;
}

export function PostFromJSON(json: any): Post {
  return PostFromJSONTyped(json, false);
}

export function PostFromJSONTyped(
  json: any,
  ignoreDiscriminator: boolean
): Post {
  if (json === undefined || json === null) {
    return json;
  }
  return {
    id: !exists(json, "id") ? undefined : json["id"],
    link: !exists(json, "link") ? undefined : json["link"],
    author: !exists(json, "author") ? undefined : json["author"],
    title: !exists(json, "title") ? undefined : json["title"],
    feed_title: !exists(json, "feed_title") ? undefined : json["feed_title"],
    pub_date: !exists(json, "pub_date")
      ? undefined
      : new Date(json["pub_date"]),
    content: !exists(json, "content") ? undefined : json["content"],
    starred: !exists(json, "starred") ? undefined : json["starred"],
    read: !exists(json, "read") ? undefined : json["read"],
  };
}

export function PostToJSON(value?: Post | null): any {
  if (value === undefined) {
    return undefined;
  }
  if (value === null) {
    return null;
  }
  return {
    starred: value.starred,
    read: value.read,
  };
}
