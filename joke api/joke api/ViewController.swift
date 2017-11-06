//
//  ViewController.swift
//  joke api
//
//  Created by Tony Cioara on 11/1/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import UIKit

struct Joke {
    let id: Int
    let type: String
    let setup: String
    let punchLine: String
    
    init(json: [String: Any]) {
        id = json["id"] as? Int ?? -1
        type = json["type"] as? String ?? ""
        setup = json["setup"] as? String ?? ""
        punchLine = json["punchline"] as? String ?? ""
    }
}

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        let url = URL(string: "https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_ten")
        
        var request = URLRequest(url: url!)
        request.httpMethod = "GET"
        
        let session = URLSession.shared
        
        let task = session.dataTask(with: request) { (data, response, error) in
            let json = try? JSONSerialization.jsonObject(with: data!, options: .allowFragments)
            let joke = Joke(json: json)
            print(joke.punchLine)
        }
        
        task.resume()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

