//
//  Networking.swift
//  product-hunt
//
//  Created by Tony Cioara on 11/3/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import Foundation

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
    static let instance = Networking()
    let session = URLSession.shared
    let baseUrl = "https://api.producthunt.com/v1"
    
    func fetch(resource: Resource, completion: @escaping (Data) -> ()) {
        
        let fullUrl = baseUrl.appending(resource.path())
        let url = URL(string: fullUrl)!
        var request = URLRequest(url: url)
        request.allHTTPHeaderFields = resource.header(token: "Bearer a226aaaa708a8a7c075988b201dca164089a2bd24987f07dfa871b999ad17fdf")
        request.httpMethod = resource.httpMethod().rawValue
        
        session.dataTask(with: request) { (data, res, err) in
            if let data = data {
            completion(data)
            }
            }.resume()
    }
}
