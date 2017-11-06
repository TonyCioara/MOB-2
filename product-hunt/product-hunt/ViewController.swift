//
//  ViewController.swift
//  product-hunt
//
//  Created by Tony Cioara on 11/1/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    var list = [Post]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        Networking.instance.fetch(resource: Resource.posts) { (data) in
            
            let posts = try? JSONDecoder().decode(PostsList.self, from: data)
            guard let allPosts = posts?.posts else {return}
            self.list = allPosts
        }
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}



