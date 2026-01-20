import { CommonModule } from "@angular/common";
import { Component, Input, OnInit, inject } from "@angular/core";
import { FileUploadService } from "../services/file-upload.service";


export interface Message {
    message: string,
    len: number,
}

@Component({
    selector: "stats-display",
    standalone: true,
    imports: [CommonModule],
    templateUrl: "./stats-display.component.html",
    styleUrl: "./stats-display.component.css",
})
export class StatsDisplay implements OnInit{
    @Input() user: string = ""
    messages: Message[] = []
    uploadService: FileUploadService = inject(FileUploadService);

    ngOnInit(): void {
        this.loadTopMessages();
    }

    loadTopMessages(){
        this.uploadService.getTopMessages(this.user, 10).subscribe({
            next: (resp) => {
                console.log(resp);
                this.messages = JSON.parse(resp);
                console.log(this.messages);
            },
            error: (err) => {
                console.error(err);
            }
        })

    }
}
