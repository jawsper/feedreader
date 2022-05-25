
export interface IToast {
  caption: string;
  message: string;
  success: boolean;
}

export interface IOutline {
  id: number;
  title: string
  unread_count: number
  feed_id: number | null
  icon: string | null
  folder_opened: boolean
  children: IOutline[]
}
