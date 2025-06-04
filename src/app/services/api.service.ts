import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";


@Injectable({
    providedIn: 'root'
})

export class ApiService {
    private djangoUrl = 'http://localhost:8000/api/';  

    constructor(private http: HttpClient) {}

    startRecording(): Observable<any>{
        return this.http.get<any>(this.djangoUrl+'record/?action=start', {});
    }

}