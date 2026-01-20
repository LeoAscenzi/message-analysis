import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UploadResponse{
    rows_added: number,
    total_rows: number,
    success_files: string[],
    failed_files: string[]

}

@Injectable({
  providedIn: 'root'
})
export class FileUploadService{

    private url = "http://localhost:8000";

    constructor(private http: HttpClient) {}

    uploadFiles(files: File[]): Observable<UploadResponse> {
        const formData = new FormData();

        files.forEach((file) => {
            formData.append("files", file);
        })

        return this.http.post<UploadResponse>(`${this.url}/upload-messages-json/`, formData);
    }

    getUsers(): Observable<any> {
        return this.http.get<any>(`${this.url}/get-users`);
    }
    
    clearData(): Observable<string> {
        return this.http.get<string>(`${this.url}/clear-data`);
    }

    getTopMessages(username: string, n: number): Observable<any> {
        return this.http.get<any>(`${this.url}/get-top-messages?username=${username}&n=${n}`);
    }
}