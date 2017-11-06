//
//  TableViewController.swift
//  product-hunt
//
//  Created by Tony Cioara on 11/5/17.
//  Copyright © 2017 Tony Cioara. All rights reserved.
//

import UIKit

class TableViewController: UITableViewController {

    var list: [Post] = [] {
        didSet {
            DispatchQueue.main.async {
                self.tableView.reloadData()
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        Networking.instance.fetch(resource: Resource.posts) { (data) in
            
            let posts = try? JSONDecoder().decode(PostsList.self, from: data)
            guard let allPosts = posts?.posts else {return}
            self.list = allPosts
            print(self.list)
            DispatchQueue.main.async {
                self.tableView.reloadData()
            }
        }
        
       
      
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return list.count
    }

    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell", for: indexPath)
    let posts = list[indexPath.row]
        cell.textLabel?.text = posts.name
        cell.detailTextLabel?.text = posts.tagline
//        cell.imageView?.image
        return cell
    }
 

}
