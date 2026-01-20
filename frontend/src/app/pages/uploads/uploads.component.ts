import { Component } from "@angular/core";
import { RouterModule } from '@angular/router';
import { FileUploadService } from "../../services/file-upload.service";
import { CommonModule } from "@angular/common";

@Component({
    selector: 'app-uploads',
    standalone: true,
    imports: [RouterModule, CommonModule],
    providers: [FileUploadService],
    templateUrl: './uploads.component.html'
})

export class UploadsComponent {

    selectedFiles: File[] = [];

    constructor(private uploadService: FileUploadService) {}

    onFileSelect(event: Event): void {
        const input = event.target as HTMLInputElement;
        if(input.files){
            this.selectedFiles = Array.from(input.files);
        }
        console.log(this.selectedFiles)
    }

    uploadFiles(): void {
        if(this.selectedFiles.length == 0){
            console.error("No files present to upload");
            return;
        }
        
        this.uploadService.uploadFiles(this.selectedFiles).subscribe({
            next: (response) => {
                console.log(response);
            },
            error: (err) =>
            {
                console.error(err);
            }
        })
    }

};