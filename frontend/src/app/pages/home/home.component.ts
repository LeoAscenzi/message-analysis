import { Component, OnInit, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FileUploadService } from '../../services/file-upload.service';
import { CommonModule } from '@angular/common';
import { StatsDisplay } from '../../stats-display/stats-display.component';

@Component({
    selector: "app-home",
    standalone: true,
    imports: [RouterModule, CommonModule, StatsDisplay],
    templateUrl: './home.component.html',
    styleUrl: './home.component.css',
})
export class HomeComponent implements OnInit {

    users: string[] = []
    targetedUser:string = "";
    uploadService: FileUploadService = inject(FileUploadService);

    ngOnInit(): void {
        this.getUsers();
    }

    getUsers(): void {
        this.uploadService.getUsers().subscribe({
            next: (resp) => {
                console.log(resp);
                this.users = resp;
            },
            error: (err) => {
                console.error(err);
            }
        })
    }

    clearData(): void {
        this.uploadService.clearData().subscribe({
            next: (resp) => {
                console.log(resp);
            },
            error: (err) => {
                console.error(err);
            }
        })
    }

};
