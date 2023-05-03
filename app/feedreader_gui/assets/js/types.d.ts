export interface IToast {
  caption: string;
  message: string;
  success: boolean;
}

export interface FolderOpen {
  id: number;
  open: boolean;
}

export interface OpenOutline {
  id: number;
}

export interface PostStarred {
  id: number
  starred: boolean
}

export interface PostRead {
  id: number
  read: boolean;
}

export interface PostFocus {
  id: number;
}
