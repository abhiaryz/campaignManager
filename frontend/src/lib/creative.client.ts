

import { Creative, CreativeFormData } from '@/types/creative';
import axiosInstance from './axios-instance';
import { utils } from './common-utils';


class CreativeClient {
   
    async getCreatives(pageNo:number,query:string): Promise<{count:number,data: Creative[]}> {
      try {
        const uri = query && query!==""? `/api/creatives/?page=${pageNo}&query=${query}`
          :`/api/creatives/?page=${pageNo}`;
        const response = await axiosInstance.get(uri, {
          headers: { 'Content-Type': 'application/json' },
        });
        return {count: response.data.count,data:response.data.results.data};
      } catch (error: any) {
        throw new Error(utils.handleErrorMessage(error));
      }
    }

    async createCreative(data: CreativeFormData): Promise<Boolean> {
        try {
            await axiosInstance.post('/api/creatives/', data);
            return true
        } catch (error: any) {
            throw new Error(utils.handleErrorMessage(error));
        }
    }
}

export const creativeClient = new CreativeClient();