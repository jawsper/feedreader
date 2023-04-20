import { api } from "./base";

export const add_new_feed = async (feed_xml_url: string) => {
  return await api.createNewFeed({
    newFeed: {
      xml_url: feed_xml_url,
    },
  });
};
