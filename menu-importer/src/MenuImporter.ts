#!/usr/bin/env ts-node

import * as dotenv from 'dotenv';
// import { FieldTypeDefinition, TypeFieldSchema } from "../../templates/reactjs/src/object-actions/types/types";
import ApiClient, {HttpResponse} from "./ApiClient";
import fs from 'fs';

const FormData = require('form-data');

dotenv.config();

type MenusData = { [key: string]: HttpResponse<any>[] }

export class MenuImporter {
    private responses: MenusData;
    private apiClient: ApiClient;

    constructor() {
        this.responses = {};
        this.apiClient = new ApiClient();
    }


    async login(): Promise<boolean> {
        const loginResponse = await this.apiClient.login(process.env.REACT_APP_LOGIN_EMAIL || '', process.env.REACT_APP_LOGIN_PASS || '')
        if (loginResponse.success) {
            console.log('Login successful, token: ', loginResponse.data);
            return true
        } else {
            console.error('Login failed:', loginResponse.error);
        }
        return false
    }

    async check_exists(): Promise<boolean> {
        const loginResponse = await this.apiClient.get()
        if (loginResponse.success) {
            console.log('Login successful, token: ', loginResponse.data);
            return true
        } else {
            console.error('Login failed:', loginResponse.error);
        }
        return false
    }

    public async createPlans() {

    }

    public async importMeals(filePath:string) {
        const headers: any = {
            'accept': 'application/json'

        }
        headers["Content-Type"] = "application/json"
        const item = {
            type: "meal"
        }
        const apiUrl = `${process.env.REACT_APP_API_HOST}/api/meal/`

        const meal_json = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        for (const meal of meal_json) {
            /*
            if (Array.isArray(meal.ingredients)) {
                const ingredientApi = `${process.env.REACT_APP_API_HOST}/api/ingredients/`
                meal.ingredients.forEach(ingredient => {
                    const topass = {
                        "name": ingredient
                    }
                    const response_ingredient = await this.apiClient.post(ingredientApi, topass, headers);
                    if (typeof this.responses['ingredient'] === 'undefined') this.responses['ingredient'] = [];
                    this.responses['ingredient'].push(response_ingredient);
                    console.log(`Created Ingredient --- ${JSON.stringify(response.data)}`)
                })
            }
             */
            const entry = {
                "title": meal.title,
                "description": meal.description,
                "bld": meal.bld,
                "price": meal.public_price
            }
            const response = await this.apiClient.post(apiUrl, entry, headers);
            if (typeof this.responses['meal'] === 'undefined') this.responses['meal'] = [];
            this.responses['meal'].push(response);
            console.log(`Created Meal --- ${JSON.stringify(response.data)}`)

        }
    }

}

const builder = new MenuImporter();
const success = await builder.login()
if (success) {
    const menu_path = "/Users/elitaylor/Developer/sammie/nod-frontend/public/api/postpartum.json";
    builder.importMeals(menu_path, "PostPartum")
}