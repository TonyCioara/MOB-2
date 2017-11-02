//
//  ViewController.swift
//  product-hunt
//
//  Created by Tony Cioara on 11/1/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import UIKit

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
}

enum Resource {
    case posts
    case comments(postId: String)
    
    func httpMethod() -> HTTPMethod {
        switch self {
        case .posts, .comments:
            return .get
        }
    }
    
    func header(token: String) -> [String: String] {
        switch self {
        case .posts, .comments:
            return [
                "Authorization": "\(token)",
                "Content-Type": "application/json"
            ]
        }
    }
    
    func path() -> String {
        switch self {
        case .posts:
            return "/me/feed"
        case .comments:
            return "/comments"
        }
    }
    
    func urlParameteres() -> [String: String] {
        switch self {
        case .comments(let postId):
            return ["search_id": postId]
        case .posts:
            return [:]
        }
    }
    
    func body() -> Data? {
        switch self {
        case .comments, .posts:
            return nil
        }
        
    }
}

class Networking {
    let session = URLSession.shared
    let baseUrl = "https://api.producthunt.com/v1"
    
    func fetch(resource: Resource, completion: @escaping () -> ()) {
        
        let fullUrl = baseUrl.appending(resource.path())
        let url = URL(string: fullUrl)!
        var request = URLRequest(url: url)
        request.allHTTPHeaderFields = resource.header(token: "a226aaaa708a8a7c075988b201dca164089a2bd24987f07dfa871b999ad17fdf")
        request.httpMethod = resource.httpMethod().rawValue
        
        session.dataTask(with: request) { (data, res, err) in
            completion()
        }.resume()
    }
}

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

