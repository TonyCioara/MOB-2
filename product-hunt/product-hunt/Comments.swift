//
//  Comments.swift
//  product-hunt
//
//  Created by Tony Cioara on 11/3/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import Foundation

struct CommentsList: Decodable {
    var comments: [Comment]
}

struct Comment {
    var id: Int
    var body: String
    var name: String
}

extension Comment: Decodable {
    enum CommentKeys: String, CodingKey {
        case id
        case body
        case name
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CommentKeys.self)
        
        let id = try container.decode(Int.self, forKey: .id)
        let body = try container.decode(String.self, forKey: .body)
        let name = try container.decode(String.self, forKey: .name)
        
        self.init(id: id, body: body, name: name)
    }
}
