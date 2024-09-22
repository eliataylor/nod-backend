#!/usr/bin/env ts-node

import * as dotenv from 'dotenv';
import ApiClient, {HttpResponse} from "./ApiClient";
import fs from 'fs';
import natural from 'natural';

dotenv.config();

type MenusData = { [key: string]: HttpResponse<any>[] }

export class MenuImporter {
    private responses: MenusData;
    private apiClient: ApiClient;

    private plans = [
        {name: "ALL-ORGANIC MENU for Colonic Clients"},
        {name: "Juice Cleanse Menu"},
        {name: "APP-DELIVERY MENU"},
        {name: "ALL-ORGANIC CATERING MENU"},
        {name: "Post Op Recovery Meal Prep"},
        {name: "POST-PARTUM MEAL PREP MENU"}
    ]

    constructor() {
        this.responses = {};
        this.apiClient = new ApiClient();
    }

    async init() {
        const success = await this.login()
        if (success) {
            this.createPlans()

            const menu_path = "/Users/elitaylor/Developer/sammie/nod-frontend/public/api/postpartum.json";
            this.importMeals(menu_path)
        }
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

    async check_exists(type: string, params: any): Promise<boolean> {
        const searchParams = new URLSearchParams(params);
        const exists = await this.apiClient.get(`${process.env.REACT_APP_API_HOST}/api/${type}/?${searchParams.toString()}`)
        // @ts-ignore
        if (exists.success && exists.data && exists.data?.results && exists.data.results.length > 0) {
            console.log('EXISTS!', exists.data);
            return true
        } else {
            console.error(`No such ${type} by ${params}`);
        }
        return false
    }

    public async createPlans() {
        for (let plan of this.plans) {
            const exists = await this.check_exists('plans', plan);
            if (!exists) {
                const response = await this.apiClient.post(`${process.env.REACT_APP_API_HOST}/api/plans/`, plan);
                if (typeof this.responses['plans'] === 'undefined') this.responses['plans'] = [];
                this.responses['plans'].push(response);
                console.log(`Created plan --- ${JSON.stringify(response.data)}`)
            }
        }
    }

    public async importMeals(filePath: string) {
        const headers: any = {
            'accept': 'application/json'

        }
        headers["Content-Type"] = "application/json"
        const item = {
            type: "meals"
        }
        const apiUrl = `${process.env.REACT_APP_API_HOST}/api/meals/`

        const meal_json = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        for (const meal of meal_json) {
            if (Array.isArray(meal.ingredients)) {
                const adjectives = this.parseIngredients(meal.ingredients);
                if (adjectives.length > 0) {
                    console.log(adjectives)
                }
                meal.ingredients = [];

                const ingredientApi = `${process.env.REACT_APP_API_HOST}/api/ingredients/`
                for (let ingredient of meal.ingredients) {
                    const exists = await this.check_exists('ingredients', ingredient);
                    if (!exists) {
                        const topass = {"name": ingredient}
                        const response_ingredient = await this.apiClient.post(ingredientApi, topass, headers);
                        if (typeof this.responses['ingredient'] === 'undefined') this.responses['ingredient'] = [];
                        this.responses['ingredient'].push(response_ingredient);
                        console.log(`Created Ingredient --- ${JSON.stringify(response_ingredient.data)}`)
                        meal.ingredients.push(response_ingredient.data.id)
                    }
                }
            }

            const exists = await this.check_exists('meals', meal);
            if (!exists) {
                const entry = {
                    "title": meal.title,
                    "description": meal.description,
                    "bld": meal.bld,
                    "price": meal.public_price
                }
                const response = await this.apiClient.post(apiUrl, entry, headers);
                if (typeof this.responses['meals'] === 'undefined') this.responses['meals'] = [];
                this.responses['meals'].push(response);
                console.log(`Created Meal --- ${JSON.stringify(response.data)}`)
            }
        }
    }

    public parseIngredients(ingredients: string[]): string[] {
        const tokenizer = new natural.WordTokenizer();
        const lexicon = new natural.Lexicon('EN', 'NN');
        const ruleSet = new natural.RuleSet('EN');
        const tagger = new natural.BrillPOSTagger(lexicon, ruleSet);
        const adjectives: string[] = [];

        ingredients.forEach(ingredient => {
            const tokens = tokenizer.tokenize(ingredient);
            const taggedTokens = tagger.tag(tokens).taggedWords;

            taggedTokens.forEach(taggedToken => {
                if (taggedToken.tag.startsWith('JJ') || taggedToken.tag.startsWith('RB')) {
                    adjectives.push(taggedToken.token);
                } else {
                    console.log(taggedToken.token)
                }
            });
        });
        return adjectives
    }

}

const builder = new MenuImporter();
builder.init()