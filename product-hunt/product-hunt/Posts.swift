//
//  Posts.swift
//  product-hunt
//
//  Created by Tony Cioara on 11/3/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import Foundation

struct PostsList: Decodable {
    var posts: [Post]
}

struct Post {
    var id: Int
    var name: String
    var tagline: String
    var votesCount: Int
}

extension Post: Decodable {
    enum PostKeys: String, CodingKey {
        case id
        case name
        case tagline
        case votesCount = "votes_count"

    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: PostKeys.self)
        
        let id = try container.decode(Int.self, forKey: .id)
        let name = try container.decode(String.self, forKey: .name)
        let tagline = try container.decode(String.self, forKey: .tagline)
        let votesCount = try container.decode(Int.self, forKey: .votesCount)
        
        self.init(id: id, name: name, tagline: tagline, votesCount: votesCount)
    }
}
