import type { IOutline } from "../types";

export type TSortOrder = "ASC" | "DESC";

export interface IPost {
  id: number;
  link: string;
  author: string;
  title: string;
  feedTitle: string;
  pubDate: string;
  content: string;
}

export interface IUserPost extends IPost {
  starred: boolean;
  read: boolean;
}

export interface ICurrentOutline {
  id: number;
  title: string;
  html_url: string | null;
  is_feed: boolean;
  show_only_new: boolean;
  sort_order: TSortOrder;
  skip: number;
  unread_count: number;
  next_page: unknown;
}

export interface IGetPostsResult extends Omit<ICurrentOutline, "id"> {
  success: boolean;
  posts: IUserPost[];
}

export interface IGetUnreadResult {
  success: boolean;
  counts: {
    [id: string]: number;
  };
  total: number;
}

export interface IPostActionResult {
  success: boolean;
  caption: string;
  message: string;
}

export interface IGetAllOutlinesResult {
  outlines: IOutline[];
}
