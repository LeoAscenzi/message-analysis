import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FileUploadService } from '../../services/file-upload.service';
import { CommonModule } from '@angular/common';

export interface Message {
    message: string,
    len: number,
}

@Component({
    selector: "app-home",
    standalone: true,
    imports: [RouterModule, CommonModule],
    templateUrl: './home.component.html',
})
export class HomeComponent {

    messages: Message[] = []
    targetedUser:string = "";
    constructor(private uploadService: FileUploadService) {}

    getTopMessages(username: string, n: number): void {
        if(this.targetedUser == "")
        {
            console.error("No user specified");
            return;
        }
        this.uploadService.getTopMessages(username, n).subscribe({
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

    updateUser(event: Event): void {
        const input = event.target as HTMLInputElement;
        this.targetedUser = input.value;
        console.log(this.targetedUser);
    }
};