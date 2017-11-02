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
        
        let jsonURLString = "https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_ten"
        guard let url = URL(string: jsonURLString) else {return}
        
        URLSession.shared.dataTask(with: url) { (data, response, err) in
            guard let data = data else {return}
            
            do {
                guard let json = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any?] else {return}
                
                let joke = Joke(json: json)
                print(joke.punchLine)
            }
            catch let jsonErr {
                print("error serializing json:", jsonErr)
            }
        }.resume()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

