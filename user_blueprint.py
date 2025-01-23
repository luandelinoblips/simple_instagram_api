from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint
from user_schema import UserSchema
from user_dataclass import User, Post
from utils import strategy_remove_spaces, strategy_remove_inner_underscores, try_username_with_strategies


blp = Blueprint('users', 'users', url_prefix='/users')

@blp.route("/<user_insta>")
class UserResource(MethodView):
    
    @blp.response(200, UserSchema)
    def get(self, user_insta):
        
        strategies = [
            strategy_remove_spaces,
            strategy_remove_inner_underscores,
        ]

        user_data = try_username_with_strategies(user_insta, strategies)
        if user_data:
            user = User(
                _id=user_data.get("id", ""),
                name=user_data.get("full_name", "Nome não disponível"),
                username=user_data.get("username", ""),
                img_url=user_data.get("profile_pic_url_hd", ""),
                email=user_data.get("business_email", ""),
                bio=user_data.get("biography", ""),
                followers=user_data.get("edge_followed_by", {}).get("count", 0),
                following=user_data.get("edge_follow", {}).get("count", 0),
                num_posts=user_data.get("edge_owner_to_timeline_media", {}).get("count", 0),
                category_name=user_data.get("category_name", "")
            )

            for post in user_data.get("edge_owner_to_timeline_media").get("edges"):
                post_node = post['node']
                post_node_comment = post_node.get("edge_media_to_caption", {}).get("edges", []) 
                dt_object = datetime.fromtimestamp(post_node.get("taken_at_timestamp", 0))
                
                post_caption = (
                    post_node_comment[0].get("node", {}).get("text", "") if post_node_comment else ""
                )
                
                post = Post(
                    _id=post_node.get('id', ""),
                    type=post_node.get('__typename', ""),
                    caption=post_caption,
                    media_url=post_node.get("video_url", ""),
                    permalink="https://www.instagram.com/p/"+post_node.get("shortcode", ""),
                    timestamp=dt_object.strftime('%Y-%m-%dT%H:%M:%s'),
                    like_count=post_node.get("edge_liked_by", {}).get("count", 0),
                    comments_count=post_node.get("edge_media_to_comment", {}).get("count", 0),
                    is_video=post_node.get("is_video"),
                    has_audio=post_node.get("has_audio")
                )
                user.posts.append(post.to_json())
            return user
        return {"message": "Perfil não encontrado!"}, 404