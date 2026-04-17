# Complete Method Reference

This file is generated from public methods in `src/storylinez/*.py` client classes.

Use this as the canonical quick reference for available SDK calls.

Notes:

- Includes methods from classes ending with `Client`.
- Excludes private/internal methods beginning with `_`.
- Method defaults are shown as parsed from source.
- Regenerate this file when module APIs change.

---

## `brand` - `BrandClient`
- `validate_rgb(color)`
- `validate_logo_key(logo_key)`
- `get_logo_upload_url(filename, org_id=None)`
- `download_logo_from_url(logo_url, org_id=None)`
- `upload_logo(file_path, org_id=None, name=None, is_default=False, is_public=False, create_brand=True, **kwargs)`
- `create(name, org_id=None, logo_key=None, upload_id=None, is_default=False, is_public=False, outro_bg_color=None, outro_logo_size=None, outro_logo_mode=None, outro_transition=None, outro_transition_duration=None, company_font=None, company_font_size=None, subtext_font=None, subtext_font_size=None, text_spacing=None, logo_text_spacing=None, main_text_color=None, sub_text_color=None, transition_duration=None, text_transition=None, text_transition_delay=None, text_transition_duration=None, cta_text_color=None, cta_subtext_color=None, cta_company_font_size=None, cta_subtext_font_size=None, cta_bg_color=None, subtitle_font_size=None, subtitle_font=None, subtitle_color=None, subtitle_bg_color=None, subtitle_bg_opacity=None, subtitle_bg_padding=None, subtitle_bg_rounded=None, subtitle_bg_corner_radius=None, subtitle_position=None, subtitle_squeeze_xp=None, subtitle_max_group_size=None, template_heading_font_size=None, template_heading_color=None, template_description_font_size=None, template_description_color=None, template_bg_color=None, template_bg_opacity=None, template_heading_font=None, template_description_font=None, template_text_spacing=None, template_xp=None, template_yp=None, template_text_align=None, template_text_transition=None, template_text_transition_delay=None, template_text_transition_duration=None, template_bg_rounded=None, template_bg_corner_radius=None, image_slideshow=None, **kwargs)`
- `get_all(org_id=None, page=1, limit=10, include_urls=True)`
- `get(brand_id=None, org_id=None)`
- `get_default(org_id=None)`
- `update(brand_id, name=None, is_default=None, is_public=None, logo_key=None, logo_upload_id=None, upload_id=None, outro_bg_color=None, outro_logo_size=None, outro_logo_mode=None, outro_transition=None, outro_transition_duration=None, company_font=None, company_font_size=None, subtext_font=None, subtext_font_size=None, text_spacing=None, logo_text_spacing=None, main_text_color=None, sub_text_color=None, transition_duration=None, text_transition=None, text_transition_delay=None, text_transition_duration=None, cta_text_color=None, cta_subtext_color=None, cta_company_font_size=None, cta_subtext_font_size=None, cta_bg_color=None, subtitle_font_size=None, subtitle_font=None, subtitle_color=None, subtitle_bg_color=None, subtitle_bg_opacity=None, subtitle_bg_padding=None, subtitle_bg_rounded=None, subtitle_bg_corner_radius=None, subtitle_position=None, subtitle_squeeze_xp=None, subtitle_max_group_size=None, template_heading_font_size=None, template_heading_color=None, template_description_font_size=None, template_description_color=None, template_bg_color=None, template_bg_opacity=None, template_heading_font=None, template_description_font=None, template_text_spacing=None, template_xp=None, template_yp=None, template_text_align=None, template_text_transition=None, template_text_transition_delay=None, template_text_transition_duration=None, template_bg_rounded=None, template_bg_corner_radius=None, image_slideshow=None, **kwargs)`
- `delete(brand_id)`
- `set_default(brand_id)`
- `add_logo(brand_id, upload_id=None, logo_key=None)`
- `duplicate(brand_id, org_id=None, name=None)`
- `get_fonts()`
- `get_public_brands(exclude_org_id=None, page=1, limit=20, include_logos=False, sort_by='updated_at', sort_order='asc', smart_sort=True)`
- `search(query='', include_public=True, org_id=None, page=1, limit=20, include_logos=False)`
- `create_or_update_brand_with_logo(name, logo_path, brand_id=None, org_id=None, **brand_params)`
- `find_or_create_default_brand(org_id=None, brand_name='Default Brand', create_if_missing=True, **brand_params)`
- `update_brand_with_logo(brand_id, logo_path, **brand_params)`
- `like(brand_id, **kwargs)`
- `dislike(brand_id, **kwargs)`
- `remove_interaction(brand_id, **kwargs)`
- `add_comment(brand_id, text=None, parent_comment_id=None, **kwargs)`
- `get_comments(brand_id, page=1, limit=10, parent_comment_id=None, **kwargs)`
- `update_comment(comment_id, text=None, **kwargs)`
- `delete_comment(comment_id, **kwargs)`

## `company_details` - `CompanyDetailsClient`
- `create(company_name, company_type='', tag_line='', vision='', products='', description='', cta_text='', cta_subtext='', link='', is_default=False, others=None, org_id=None, profile_type='', **kwargs)`
- `get_all(page=1, limit=10, sort_by='created_at', order='desc', org_id=None, **kwargs)`
- `get_one(company_details_id=None, org_id=None, **kwargs)`
- `get_default(org_id=None, **kwargs)`
- `update(company_details_id, company_name=None, company_type=None, tag_line=None, vision=None, products=None, description=None, cta_text=None, cta_subtext=None, link=None, is_default=None, others=None, profile_type=None, **kwargs)`
- `delete(company_details_id, **kwargs)`
- `set_default(company_details_id, **kwargs)`
- `duplicate(company_details_id, company_name=None, org_id=None, **kwargs)`
- `search(query='', field='company_name', page=1, limit=10, sort_by='created_at', order='desc', org_id=None, **kwargs)`
- `find_or_create_default_company(company_name=None, create_if_missing=True, company_type='', tag_line='', vision='', products='', description='', org_id=None, **kwargs)`

## `data_collection` - `DataCollectionClient`
- `status()`
- `start_youtube_collection(org_id=None, query=None, prompt=None, instructions=None, max_results=None, name=None, description=None)`
- `get_youtube_job(job_id, org_id=None)`
- `list_youtube_jobs(org_id=None, page=1, page_size=20, search=None, status=None, sort_by=None, sort_direction=None)`
- `start_youtube_extraction(job_id, video_indices, org_id=None)`
- `get_youtube_extraction_status(job_id, org_id=None)`
- `get_youtube_item_url(job_id, item_index, org_id=None, expiry=3600)`

## `pipeline` - `PipelineClient`
- `run_web_scraping_and_brand_extraction(website_url, timeout=60, depth=1, enable_js=False, include_palette=True, dynamic_extraction=False, deepthink=False, overdrive=False, web_search=False, eco=False, polling_interval=10)`

## `pipeline_jobs` - `PipelineJobsClient`
- `status()`
- `start_v1(label, org_id=None, main_prompt=None, reference_video_id=None, **config)`
- `start_v2(label, sequence_prompt, org_id=None, **config)`
- `get_job(job_id)`
- `get_job_status(job_id)`
- `get_job_result(job_id)`
- `cancel_job(job_id)`

## `project` - `ProjectClient`
- `create_folder(name, description='', org_id=None, label_icon=None, label_color=None)`
- `get_all_folders(org_id=None)`
- `update_folder(folder_id, name=None, description=None, label_icon=None, label_color=None)`
- `delete_folder(folder_id, move_projects=False)`
- `search_folders(query='', search_fields=None, created_after=None, created_before=None, updated_after=None, updated_before=None, created_by=None, page=1, limit=10, sort_by='created_at', sort_order='desc', org_id=None)`
- `create_project(name, orientation, purpose='', target_audience='', folder_id=None, company_details_id=None, brand_id=None, associated_files=None, settings=None, org_id=None, project_type='v1')`
- `get_all_projects(status=None, generate_thumbnail_links=False, page=1, limit=10, sort_by='created_at', sort_order='desc', org_id=None)`
- `get_project(project_id, generate_thumbnail_links=False)`
- `update_project(project_id, name=None, purpose=None, target_audience=None, company_details_id=None, brand_id=None, settings=None, project_type=None)`
- `update_project_status(project_id, status)`
- `delete_project(project_id)`
- `duplicate_project(project_id, name=None, project_type=None)`
- `move_project_to_folder(project_id, folder_id=None)`
- `search_projects(query='', search_fields=None, status=None, folder_id=None, orientation=None, brand_id=None, company_details_id=None, created_by=None, created_after=None, created_before=None, updated_after=None, updated_before=None, page=1, limit=10, sort_by='created_at', sort_order='desc', generate_thumbnail_links=False, org_id=None)`
- `get_projects_by_folder(folder_id=None, page=1, limit=10, sort_by='created_at', sort_order='desc', generate_thumbnail_links=False, org_id=None)`
- `get_projects_by_status(status, folder_id=None, page=1, limit=10, sort_by='created_at', sort_order='desc', generate_thumbnail_links=False, org_id=None)`
- `get_unrendered_projects(org_id=None, project_type=None, page=1, limit=10, sort_by='updated_at', sort_order='desc')`
- `add_associated_file(project_id, file_id, project_type=None)`
- `add_associated_files_bulk(project_id, file_ids, project_type=None)`
- `remove_associated_file(project_id, file_id, project_type=None)`
- `add_stock_file(project_id, stock_id, media_type, project_type=None)`
- `add_stock_files_bulk(project_id, stock_ids, media_type, project_type=None)`
- `remove_stock_file(project_id, stock_id, media_type, project_type=None)`
- `get_project_files(project_id, include_details=False, generate_thumbnail_links=False, generate_streamable_links=False, project_type=None)`
- `add_voiceover(project_id, file_id, voice_name='Custom Voiceover', project_type=None)`
- `add_voiceovers_bulk(project_id, voiceovers, selected_index=0, project_type=None)`
- `remove_voiceover(project_id, project_type=None)`
- `get_voiceover(project_id, include_details=False, project_type=None)`
- `create_project_with_files(name, orientation, files=None, folder_name=None, purpose='', target_audience='', settings=None, org_id=None, project_type='v1')`

## `prompt` - `PromptClient`
- `create_text_prompt(project_id, main_prompt, document_context='', temperature=0.7, total_length=20, iterations=1, deepthink=False, overdrive=False, web_search=False, eco=False, skip_voiceover=False, voiceover_mode='generated', engine=None, model=None, enable_content_analysis=True, project_type=None)`
- `create_video_prompt(project_id, reference_video_id, temperature=0.7, total_length=20, iterations=1, deepthink=False, overdrive=False, web_search=False, eco=False, skip_voiceover=False, voiceover_mode='generated', include_detailed_analysis=False, engine=None, model=None, enable_content_analysis=True, project_type=None)`
- `create_prompt(project_id, **kwargs)`
- `get_prompt(prompt_id=None, project_id=None)`
- `get_prompt_by_project(project_id)`
- `update_prompt(prompt_id=None, project_id=None, temperature=None, total_length=None, iterations=None, deepthink=None, overdrive=None, web_search=None, eco=None, main_prompt=None, document_context=None, reference_video_id=None, skip_voiceover=None, voiceover_mode=None, engine=None, model=None)`
- `selfupdate_prompt(prompt_id=None, project_id=None)`
- `switch_to_text_prompt(prompt_id, main_prompt, document_context='')`
- `switch_to_video_prompt(prompt_id, reference_video_id, include_detailed_analysis=False)`
- `switch_prompt_type(prompt_id, **kwargs)`
- `get_reference_video_upload_link(filename, org_id=None, file_size=0)`
- `complete_reference_video_upload(upload_id=None, key=None, org_id=None, filename=None, mimetype=None, context='', tags=None, company_details='', analyze_audio=True, deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, advanced_detection=True, model=None)`
- `list_reference_videos(org_id=None, detailed=False, generate_thumbnail=True, generate_streamable=False, generate_download=False, include_usage=False, max_prompts_per_video=5, page=1, limit=10)`
- `get_reference_video_details(file_id, detailed=True, generate_thumbnail=True, generate_streamable=True, generate_download=True, include_usage=True)`
- `search_reference_videos(query, org_id=None, page=1, limit=10, detailed=False, generate_thumbnail=True, generate_streamable=False, generate_download=False, include_usage=False, max_prompts_per_video=5)`
- `delete_reference_video(file_id)`
- `get_reference_videos_by_ids(file_ids, org_id=None, detailed=False, generate_thumbnail=True, generate_streamable=False, generate_download=False, include_usage=False)`
- `upload_reference_video(file_path, org_id=None, context='', tags=None, company_details='', analyze_audio=True, deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, advanced_detection=True, model=None)`
- `batch_upload_reference_videos(file_paths, org_id=None, context='', tags=None, analyze_audio=True)`
- `generate_search_query(prompt_id=None, project_id=None, num_videos=5, num_audio=1, num_images=0, company_details='', documents=None, temperature=None)`
- `get_search_query_results(prompt_id=None, project_id=None, job_id=None)`
- `start_query_gen_and_wait(prompt_id=None, project_id=None, num_videos=5, num_audio=1, num_images=0, company_details='', documents=None, temperature=None, max_wait_seconds=60, poll_interval_seconds=2)`
- `get_storage_usage(org_id=None)`

## `render` - `RenderClient`
- `get_render_history(render_id=None, project_id=None, page=1, limit=10, generate_stream_link=True, generate_download_link=True, generate_thumbnail_stream_link=True)`
- `create_render(project_id, project_type=None, target_width=None, target_height=None, standardize_resolution_enabled=None, bg_music_volume=None, video_audio_volume=None, voiceover_volume=None, min_video_length=None, fallback_vo_length=None, subtitle_enabled=None, subtitle_font_size=None, subtitle_font=None, subtitle_color=None, subtitle_bg_color=None, subtitle_bg_opacity=None, subtitle_position=None, subtitle_bg_padding=None, subtitle_bg_rounded=None, subtitle_bg_corner_radius=None, subtitle_squeeze_xp=None, subtitle_max_group_size=None, outro_duration=None, outro_bg_color=None, outro_logo_size=None, outro_logo_mode=None, outro_transition=None, outro_transition_duration=None, company_name=None, company_subtext=None, call_to_action=None, call_to_action_subtext=None, link=None, enable_cta=None, company_font=None, company_font_size=None, subtext_font=None, subtext_font_size=None, text_spacing=None, logo_text_spacing=None, main_text_color=None, sub_text_color=None, cta_text_color=None, cta_subtext_color=None, cta_company_font_size=None, cta_subtext_font_size=None, cta_bg_color=None, text_transition=None, text_transition_delay=None, text_transition_duration=None, template_heading_font_size=None, template_heading_color=None, template_heading_font=None, template_description_font_size=None, template_description_color=None, template_description_font=None, template_bg_color=None, template_bg_opacity=None, template_bg_rounded=None, template_bg_corner_radius=None, template_text_spacing=None, template_xp=None, template_yp=None, template_text_align=None, template_text_transition=None, template_text_transition_delay=None, template_text_transition_duration=None, color_balance_fix=None, color_exposure_fix=None, color_contrast_fix=None, image_slideshow=None, extend_short_clips=None, extension_method=None, max_retries=None, adaptive_complexity=None, enable_emergency_mode=None, memory_threshold=None, recovery_mode=None, include_outro=None, include_branding_outro=None, watermark=None, bitrate=None, fps=None, subtitle_bridge_small_gaps_threshold=None, scene_threshold=None, scene_min_scene_duration=None, scene_min_scene_gap=None, lingering_fix_enabled=None, lingering_method=None, lingering_max_window=None, audio_lingering_fix_enabled=None, audio_lingering_max_window=None, allow_extend_last_clip=None, framing_fill_bias=None, add_blurred_background=None, blur_strength=None, background_opacity=None)`
- `get_render(render_id=None, project_id=None, include_results=True, include_sequence=False, include_subtitles=False, generate_download_link=False, generate_streamable_link=False, generate_thumbnail_stream_link=False)`
- `redo_render(render_id=None, project_id=None, project_type=None, target_width=None, target_height=None, standardize_resolution_enabled=None, bg_music_volume=None, video_audio_volume=None, voiceover_volume=None, min_video_length=None, fallback_vo_length=None, subtitle_enabled=None, subtitle_font_size=None, subtitle_font=None, subtitle_color=None, subtitle_bg_color=None, subtitle_bg_opacity=None, subtitle_position=None, subtitle_bg_padding=None, subtitle_bg_rounded=None, subtitle_bg_corner_radius=None, subtitle_squeeze_xp=None, subtitle_max_group_size=None, outro_duration=None, outro_bg_color=None, outro_logo_size=None, outro_logo_mode=None, outro_transition=None, outro_transition_duration=None, company_name=None, company_subtext=None, call_to_action=None, call_to_action_subtext=None, link=None, enable_cta=None, company_font=None, company_font_size=None, subtext_font=None, subtext_font_size=None, text_spacing=None, logo_text_spacing=None, main_text_color=None, sub_text_color=None, cta_text_color=None, cta_subtext_color=None, cta_company_font_size=None, cta_subtext_font_size=None, cta_bg_color=None, text_transition=None, text_transition_delay=None, text_transition_duration=None, template_heading_font_size=None, template_heading_color=None, template_heading_font=None, template_description_font_size=None, template_description_color=None, template_description_font=None, template_bg_color=None, template_bg_opacity=None, template_bg_rounded=None, template_bg_corner_radius=None, template_text_spacing=None, template_xp=None, template_yp=None, template_text_align=None, template_text_transition=None, template_text_transition_delay=None, template_text_transition_duration=None, color_balance_fix=None, color_exposure_fix=None, color_contrast_fix=None, image_slideshow=None, extend_short_clips=None, extension_method=None, max_retries=None, adaptive_complexity=None, enable_emergency_mode=None, memory_threshold=None, recovery_mode=None, include_outro=None, include_branding_outro=None, watermark=None, bitrate=None, fps=None, subtitle_bridge_small_gaps_threshold=None, scene_threshold=None, scene_min_scene_duration=None, scene_min_scene_gap=None, lingering_fix_enabled=None, lingering_method=None, lingering_max_window=None, audio_lingering_fix_enabled=None, audio_lingering_max_window=None, allow_extend_last_clip=None, framing_fill_bias=None, add_blurred_background=None, blur_strength=None, background_opacity=None)`
- `update_render_settings(render_id=None, project_id=None, bg_music_volume=None, video_audio_volume=None, voiceover_volume=None, subtitle_enabled=None, subtitle_font_size=None, subtitle_color=None, subtitle_bg_color=None, subtitle_bg_opacity=None, outro_duration=None, company_name=None, company_subtext=None, call_to_action=None, call_to_action_subtext=None, enable_cta=None, color_balance_fix=None, color_exposure_fix=None, color_contrast_fix=None, **kwargs)`
- `update_render(render_id=None, project_id=None, fields_to_update=None, project_type=None)`
- `get_render_status(render_id=None, project_id=None)`
- `get_render_download_links(render_id=None, project_id=None)`
- `create_and_wait_for_render(project_id, poll_interval=5, timeout=3600, auto_generate_links=True, project_type=None, **kwargs)`
- `update_settings_and_redo(render_id=None, project_id=None, wait_for_completion=False, poll_interval=5, timeout=3600, project_type=None, **kwargs)`

## `search` - `SearchClient`
- `search_video_scenes(query, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_video_objects(objects, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_content(query=None, genre=None, mood=None, instruments=None, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_combined(query, media_types=None, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_by_genre(genres, min_probability=0.1, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_by_mood(moods, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_by_instrument(instruments, min_confidence=0.5, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_by_intelligence(classes, min_confidence=0.0, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=False, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_by_harmony(chord_keywords=None, key_signatures=None, chord_progressions=None, media_source='user', folder_path=None, page=1, page_size=20, org_id=None, **kwargs)`
- `search_audio_by_transcription(query, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_image_by_objects(objects, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_image_by_color(color_moods=None, dominant_hues=None, hex_color=None, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_image_by_text(query, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_by_tags(tags, match_all=False, media_types=None, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_video_by_tags(tags, match_all=False, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_audio_by_tags(tags, match_all=False, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `search_image_by_tags(tags, match_all=False, media_source='user', folder_path=None, page=1, page_size=20, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None, **kwargs)`
- `find_similar_content(content_id, media_types=None, media_source='user', count=10, org_id=None)`
- `search_topics(topic, subtopics=None, media_types=None, media_source='user', page=1, page_size=20, org_id=None)`

## `sequence` - `SequenceClient`
- `create_sequence(project_id, apply_template=False, apply_grade=False, grade_type='single', orientation=None, deepthink=False, overdrive=False, web_search=False, eco=False, enable_content_analysis=None, temperature=0.7, iterations=1, engine=None, model_override=None, project_type=None, **kwargs)`
- `get_sequence(sequence_id=None, project_id=None, include_results=True, include_storyboard=False, **kwargs)`
- `redo_sequence(sequence_id=None, project_id=None, include_history=True, regenerate_prompt=None, engine=None, model_override=None, enable_content_analysis=None, project_type=None, **kwargs)`
- `update_sequence(sequence_id=None, project_id=None, update_ai_params=True, project_type=None, **kwargs)`
- `update_sequence_settings(sequence_id=None, project_id=None, apply_template=None, apply_grade=None, grade_type=None, orientation=None, deepthink=None, overdrive=None, web_search=None, eco=None, engine=None, model_override=None, enable_content_analysis=None, temperature=None, iterations=None, regenerate_prompt=None, edited_sequence=None, project_type=None, **kwargs)`
- `get_sequence_history(sequence_id, page=1, limit=10, history_type=None, include_current=False, **kwargs)`
- `get_sequence_media(sequence_id=None, project_id=None, include_analysis=False, generate_thumbnail=True, generate_streamable=True, generate_download=False, **kwargs)`
- `reorder_sequence_items(sequence_id, array_type, new_order, project_type=None, **kwargs)`
- `edit_sequence_item(sequence_id, item_type, item_index=None, updated_item=None, file_id=None, stock_id=None, project_type=None, **kwargs)`
- `change_sequence_media(sequence_id, item_type, item_index=None, file_id=None, stock_id=None, path=None, project_type=None, **kwargs)`
- `update_and_regenerate(sequence_id=None, project_id=None, regenerate_prompt=None, include_history=True, wait_for_completion=False, check_interval=5, timeout=600)`
- `swap_media(sequence_id, first_item_index, second_item_index, array_type='clips')`
- `send_chat_prompt(sequence_id=None, project_id=None, prompt=None, include_history=True, wait_for_completion=False, polling_interval=5, timeout=300)`
- `get_chat_history(sequence_id, limit=20, include_generations=True)`
- `restore_version(sequence_id, history_timestamp, apply_as_edit=True, regenerate=False, regenerate_prompt=None)`
- `combine_manual_and_ai_edits(sequence_id, manual_edits, ai_prompt='Refine this sequence while keeping my manual edits intact', wait_for_completion=False)`

## `settings` - `SettingsClient`
- `get_settings()`
- `get_email_preferences()`
- `update_email_preferences(preferences)`
- `save_settings(ai_params=None, temperature=None, iterations=None, deepthink=None, web_search=None, overdrive=None, eco=None, link_preferences=None, generate_thumbnail=None, generate_streamable=None, generate_download=None, detail=None, ui_preferences=None, dark_mode=None, default_view=None, language=None, current_org_id=None, last_project_id=None, current_tab=None, **kwargs)`
- `update_settings(ai_params=None, temperature=None, iterations=None, deepthink=None, web_search=None, overdrive=None, eco=None, link_preferences=None, generate_thumbnail=None, generate_streamable=None, generate_download=None, detail=None, ui_preferences=None, dark_mode=None, default_view=None, language=None, current_org_id=None, last_project_id=None, current_tab=None, **kwargs)`
- `reset_settings(category='all')`
- `update_theme(dark_mode)`
- `update_ai_defaults(temperature=None, iterations=None, deepthink=None, overdrive=None, web_search=None, eco=None)`
- `add_job(job_id, job_type='query_generation', org_id=None, project_id=None, metadata=None)`
- `list_jobs(org_id=None, project_id=None, job_type=None, page=1, limit=10, sort_by='created_at', sort_order='desc')`
- `delete_job(job_id, org_id=None)`
- `fetch_job_results(job_id, org_id=None)`
- `apply_preset(preset_name)`
- `toggle_theme()`
- `backup_settings(filename=None)`
- `restore_settings(filename)`

## `stock` - `StockClient`
- `search(queries, collections=None, detailed=False, generate_thumbnail=False, generate_streamable=False, generate_download=False, num_results=None, num_results_videos=1, num_results_audios=1, num_results_images=1, similarity_threshold=0.5, orientation=None, **kwargs)`
- `get_by_id(stock_id, media_type, detailed=True, generate_thumbnail=True, generate_streamable=False, generate_download=False, **kwargs)`
- `list_media(media_type, page=1, limit=20, sort_by='processed_at', sort_order='asc', detailed=False, generate_thumbnail=False, generate_streamable=False, generate_download=False, orientation=None, search=None, smart_sort=True, **kwargs)`
- `get_by_ids(ids, media_types, detailed=True, generate_thumbnail=True, generate_streamable=False, generate_download=False, **kwargs)`
- `search_videos(query, num_results=5, orientation=None, detailed=False, generate_thumbnail=True, generate_streamable=True)`
- `search_audios(query, num_results=5, detailed=False, generate_thumbnail=True, generate_streamable=True)`
- `search_images(query, num_results=5, detailed=False, generate_thumbnail=True)`
- `find_similar_media(stock_id, media_type, num_results=5)`
- `batch_get_items(ids_by_media_type, detailed=True, generate_thumbnail=True)`
- `like(stock_id, media_type, **kwargs)`
- `dislike(stock_id, media_type, **kwargs)`
- `remove_interaction(stock_id, media_type, **kwargs)`

## `storage` - `StorageClient`
- `wait_for_file_processing(file_id, max_wait_time=900, polling_interval=10, progress_callback=None)`
- `get_allowed_analysis_models()`
- `generate_upload_link(filename, file_size=0, folder_path='/', org_id=None)`
- `upload_file(file_path, folder_path='/', context='', tags=None, analyze_audio=True, auto_company_details=True, company_details_id='', deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, advanced_detection=True, model='auto', org_id=None, **kwargs)`
- `upload_and_process_files_bulk(file_paths, folder_path='/', context='', tags=None, analyze_audio=True, auto_company_details=True, company_details_id='', deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, advanced_detection=True, model='auto', org_id=None, progress_callback=None, poll_interval=10, **kwargs)`
- `upload_file_data(file_data, filename, folder_path='/', content_type=None, file_size=None, context='', tags=None, analyze_audio=True, auto_company_details=True, company_details_id='', deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, advanced_detection=True, model='auto', org_id=None)`
- `mark_upload_complete(upload_id, org_id=None, filename=None, mimetype=None, folder_path=None, context=None, tags=None, analyze_audio=None, auto_company_details=None, company_details_id=None, deepthink=None, overdrive=None, web_search=None, eco=None, temperature=None, advanced_detection=None, model=None, **kwargs)`
- `get_folder_contents(path='/', recursive=False, detailed=False, generate_thumbnail=True, generate_streamable=False, generate_download=False, include_protected=False, org_id=None)`
- `create_folder(folder_name, parent_path='/', org_id=None)`
- `delete_folder(folder_id, delete_contents=False)`
- `rename_folder(folder_id, new_name)`
- `move_folder(folder_id, target_parent_path)`
- `get_folder_tree(path='/', include_protected=False, org_id=None)`
- `list_folders(path='/', recursive=False, org_id=None)`
- `browse_folders(org_id=None, path='/', page=1, page_size=50, sort_by='name', sort_direction='asc')`
- `list_unused_files(org_id=None, detailed=False, generate_thumbnail=True, generate_streamable=True, generate_download=False, page=1, page_size=50, sort_by='upload_date', sort_direction='desc', cursor_value=None, cursor_id=None, max_scan_batches=8)`
- `search_files_by_name(query, path='/', recursive=False, detailed=True, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None)`
- `vector_search(queries, path=None, detailed=True, generate_thumbnail=True, generate_streamable=False, generate_download=False, num_results=10, similarity_threshold=0.5, orientation=None, file_types='all', org_id=None)`
- `get_file_analysis(file_id, detailed=True, generate_thumbnail=True, generate_streamable=True, generate_download=True)`
- `rate_file(file_id, rating)`
- `remove_file_rating(file_id)`
- `get_file_rating(file_id)`
- `get_reference_video(file_id, detailed=True, generate_thumbnail=True, generate_streamable=True, generate_download=False)`
- `delete_file(file_id)`
- `rename_file(file_id, new_name)`
- `move_file(file_id, target_folder_path)`
- `get_download_link(file_id)`
- `get_original_download_link(file_id)`
- `reprocess_file(file_id, context=None, tags=None, analyze_audio=None, auto_company_details=None, company_details_id=None, deepthink=None, overdrive=None, web_search=None, eco=None, temperature=None, **kwargs)`
- `get_files_by_ids(file_ids, detailed=False, generate_thumbnail=True, generate_streamable=False, generate_download=False, org_id=None)`
- `get_storage_usage(org_id=None)`
- `import_youtube_download(org_id, s3_key, title, original_url, folder_path='/', analyze=True, context='', tags=None, analyze_audio=True, advanced_detection=True, auto_company_details=True, company_details_id='', company_details='', deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, model=None, trim_enabled=None, trim_start_seconds=None, trim_end_seconds=None)`
- `ensure_folder_path(path, org_id=None)`
- `upload_directory(local_dir, remote_folder='/', include_subdirs=True, file_extensions=None, context='', tags=None, analyze_audio=True, auto_company_details=True, org_id=None, **kwargs)`

## `storyboard` - `StoryboardClient`
- `create_storyboard(project_id, deepthink=False, overdrive=False, web_search=False, eco=False, temperature=0.7, iterations=3, full_length=None, voiceover_mode='generated', skip_voiceover=False, documents=None, engine=None, model=None, model_override=None, project_type=None, **kwargs)`
- `get_storyboard(storyboard_id=None, project_id=None, include_results=False, include_details=False, project_type=None, **kwargs)`
- `update_storyboard(storyboard_id=None, project_id=None, update_ai_params=True, project_type=None, **kwargs)`
- `update_storyboard_values(storyboard_id=None, project_id=None, edited_storyboard=None, regeneration_prompt=None, deepthink=None, overdrive=None, web_search=None, eco=None, temperature=None, iterations=None, full_length=None, skip_voiceover=None, voiceover_mode=None, documents=None, project_type=None, **kwargs)`
- `redo_storyboard(storyboard_id=None, project_id=None, regeneration_prompt=None, include_history=False, project_type=None, **kwargs)`
- `reorder_storyboard_items(storyboard_id, array_type, new_order, **kwargs)`
- `edit_storyboard_item(storyboard_id, item_type, updated_item, item_index=None, **kwargs)`
- `change_storyboard_media(storyboard_id, item_type, item_index, file_id=None, stock_id=None, path=None, **kwargs)`
- `get_storyboard_history(storyboard_id, page=1, limit=10, history_type=None, include_current=False, **kwargs)`
- `get_storyboard_media(storyboard_id=None, project_id=None, include_analysis=False, generate_thumbnail=True, generate_streamable=True, generate_download=False, project_type=None, **kwargs)`
- `update_and_regenerate(storyboard_id=None, project_id=None, regeneration_prompt=None, update_ai_params=True, include_history=True, project_type=None)`
- `wait_for_generation_complete(job_id, polling_interval=5, timeout=300)`
- `create_storyboard_and_wait(project_id, polling_interval=5, timeout=300, project_type=None, **kwargs)`
- `create_simple_edit(storyboard_id, scene_changes)`
- `send_chat_prompt(storyboard_id=None, project_id=None, prompt=None, include_history=True, wait_for_completion=False, polling_interval=5, timeout=300, project_type=None)`
- `get_chat_history(storyboard_id, limit=20, include_generations=True)`
- `restore_version(storyboard_id, history_timestamp, apply_as_edit=True, regenerate=False, regeneration_prompt=None)`

## `tools` - `ToolsClient`
- `get_tool_types()`
- `create_creative_brief(name, user_input, org_id=None, company_details=None, auto_company_details=True, company_details_id=None, documents=None, temperature=0.7, deepthink=False, overdrive=False, web_search=False, eco=False, **kwargs)`
- `create_audience_research(name, user_input, org_id=None, company_details=None, auto_company_details=True, company_details_id=None, additional_context=None, documents=None, temperature=0.7, deepthink=True, overdrive=True, eco=False, **kwargs)`
- `create_video_plan(name, user_input, org_id=None, company_details=None, auto_company_details=True, company_details_id=None, additional_context=None, documents=None, temperature=0.7, deepthink=True, overdrive=True, eco=False, **kwargs)`
- `create_shotlist(name, user_input, org_id=None, scene_details=None, visual_style=None, documents=None, temperature=0.7, deepthink=False, overdrive=False, web_search=False, eco=False, **kwargs)`
- `create_ad_concept(name, user_input, org_id=None, brand_details=None, auto_company_details=True, company_details_id=None, campaign_goals=None, target_audience=None, documents=None, temperature=0.7, deepthink=True, overdrive=True, eco=False, **kwargs)`
- `create_scene_transitions(name, scene_descriptions, org_id=None, project_style=None, mood=None, brand_guidelines=None, auto_company_details=True, company_details_id=None, documents=None, temperature=0.7, deepthink=True, overdrive=True, eco=False, **kwargs)`
- `create_trend_analysis(name, topic, org_id=None, location='worldwide', temperature=0.7, deepthink=False, overdrive=False, eco=False, **kwargs)`
- `create_scene_splitter(name, video_path, bucket_name, org_id=None, **kwargs)`
- `create_web_scraper_advanced(name, website_url, org_id=None, depth=1, max_pages=5, max_text_chars=20000, enable_js=False, parallel=False, retry_count=2, retry_delay=1.0, timeout=15, max_batch_size=5, documents=None, deepthink=False, overdrive=False, web_search=False, eco=False, **kwargs)`
- `get_tool(tool_id, include_job=True, **kwargs)`
- `list_tools(org_id=None, tool_type=None, include_results=False, page=1, limit=20, **kwargs)`
- `update_tool(tool_id, name=None, tags=None, **kwargs)`
- `delete_tool(tool_id, **kwargs)`
- `redo_tool(tool_id, input_data=None, auto_company_details=None, company_details_id=None, deepthink=None, overdrive=None, web_search=None, eco=None, **kwargs)`
- `wait_for_tool_completion(tool_id, max_wait_time=120, polling_interval=10)`
- `create_and_wait(tool_type, name, **kwargs)`

## `user` - `UserClient`
- `get_current_user()`
- `get_user(user_id)`
- `get_users_batch(user_ids)`
- `get_user_storage(org_id=None)`
- `get_org_storage(org_id=None, include_breakdown=False)`
- `get_subscription(org_id=None)`
- `get_project_usage(org_id=None)`
- `get_extra_projects(org_id=None)`
- `get_developer_status()`

## `utils` - `UtilsClient`
- `get_supported_formats()`
- `get_voice_types()`
- `get_transition_types()`
- `get_template_types()`
- `get_color_grades()`
- `alter_prompt(old_prompt, job_name=None, company_details=None, company_details_id=None, edited_json=None, temperature=0.7, alter_type='enhance', prompt_type='prompt', org_id=None, creativity=None, sarcasm=None, formality=None, detail_level=None, urgency=None, emotional_tone=None, pacing=None, cut_frequency=None, clip_length=None, retention_focus=None, energy_level=None, narrative_structure=None)`
- `search_recommendations(user_query, job_name=None, documents=None, temperature=0.7, deepthink=False, overdrive=False, web_search=False, eco=False, org_id=None)`
- `get_organization_info(website_url, job_name=None, scraped_content=None, documents=None, chat_history=None, temperature=0.7, deepthink=True, overdrive=False, web_search=False, eco=False, org_id=None)`
- `extract_brand_settings(website_url, org_id=None, job_name=None, temperature=0.7, deepthink=True, overdrive=False, eco=False, timeout=45, include_palette=True, dynamic_extraction=False, max_elements=100, web_search=False, **kwargs)`
- `get_job_result(job_id)`
- `list_jobs(job_type=None, page=1, limit=20, org_id=None)`
- `wait_for_job_completion(job_id, timeout_seconds=60, polling_interval=10, callback=None)`
- `enhance_prompt_and_wait(prompt, **kwargs)`

## `v2_context` - `V2ContextClient`
- `add_document(project_id, content, org_id=None, title=None, summary=None, tags=None, nickname=None)`
- `list_documents(project_id, org_id=None, page=1, page_size=10, content_chars=None)`
- `get_document_page(project_id, doc_id, org_id=None, page=1, page_chars=None)`
- `update_document(project_id, doc_id, org_id=None, title=None, content=None, summary=None, tags=None, nickname=None)`
- `delete_document(project_id, doc_id, org_id=None)`
- `set_reference(project_id, org_id=None, file_id=None, ref_id=None, nickname=None)`
- `get_reference(project_id, ref_id, org_id=None)`
- `list_references(project_id, org_id=None, page=1, page_size=10)`
- `clear_reference(project_id, org_id=None, ref_id=None)`

## `v2_effects` - `V2EffectsClient`
- `get_catalog(org_id=None, project_id=None, asset_type=None, search=None, extra_params=None)`
- `list_effects(asset_type, org_id=None, project_id=None, search=None, page=None, page_size=None, extra_params=None)`
- `find_effect(effect_id, org_id=None, project_id=None, asset_type=None, search=None, extra_params=None)`

## `v2_project` - `V2ProjectClient`
- `get_generation_settings(project_id, org_id=None)`
- `add_media(project_id, org_id=None, file_id=None, stock_id=None, media_type=None)`
- `add_media_bulk(project_id, org_id=None, file_ids=None, items=None)`
- `list_media(project_id, org_id=None, include_analysis=False, page=1, page_size=20)`

## `v2_render` - `V2RenderClient`
- `start_render(project_id, org_id=None, sequence_id=None, target_width=None, target_height=None, video_bitrate=None, audio_bitrate=None, video_preset=None, watermark=None, codec=None, audio_codec=None, output_bucket=None)`
- `get_render(project_id, org_id=None, render_id=None, include_results=None, include_sequence=None, include_subtitles=None, generate_download_link=None, generate_streamable_link=None, generate_thumbnail_stream_link=None, stream_use_cdn=None, download_use_cdn=None, thumbnail_stream_use_cdn=None, page=None, page_size=None)`
- `get_history(project_id, org_id=None, render_id=None, page=None, limit=None, generate_streamable_link=None, generate_thumbnail_stream_link=None, generate_download_link=None, stream_use_cdn=None, thumbnail_stream_use_cdn=None, download_use_cdn=None)`
- `wait_for_render_completion(project_id, render_id, org_id=None, poll_interval=5.0, timeout=600.0, terminal_statuses=None, **get_kwargs)`

## `v2_schema` - `V2SchemaClient`
- `get_sequence_schema(org_id=None, project_id=None, include_examples=None, extra_params=None)`
- `get_asset_schema(org_id=None, project_id=None, asset_type=None, extra_params=None)`
- `get_all_schemas(org_id=None, project_id=None, include_examples=None, asset_types=None, sequence_extra_params=None, asset_extra_params=None)`

## `v2_sequence` - `V2SequenceClient`
- `create_session(project_id, org_id=None, message='', temperature=0.7, model_override=None, eco=None)`
- `continue_session(project_id, org_id=None, message='', temperature=0.7, model_override=None, eco=None)`
- `stop_session(project_id, org_id=None, session_id=None)`
- `list_sequences(project_id, org_id=None, page=None, page_size=None)`
- `list_sequences_lite(project_id, org_id=None)`
- `get_sequence(project_id, org_id=None, sequence_id=None)`
- `list_sequence_media(project_id, org_id=None, sequence_id=None, include_analysis=False)`
- `update_sequence(project_id, sequence_id, sequence, org_id=None, session_id=None, validate_only=False)`
- `import_asset(project_id, tool_name, parameters, org_id=None, session_id=None, sequence_id=None)`
- `list_snapshots(project_id, session_id, sequence_id, org_id=None, page=None, page_size=None)`
- `get_history(project_id, session_id, org_id=None, sequence_id=None, page=None, page_size=None, bearer_token=None)`
- `wait_for_job_completion(project_id, org_id=None, sequence_id=None, poll_interval=5.0, timeout=300.0, terminal_statuses=None)`

## `v2_share` - `V2ShareClient`
- `create_share(project_id, render_id, org_id=None, sequence_id=None, render_s3_key=None)`
- `get_public_share(share_id, generate_streamable_link=True, stream_use_cdn=False)`
- `list_shares(project_id, org_id=None, page=1, limit=20)`
- `revoke_share(share_id, org_id=None)`

## `voice_library` - `VoiceLibraryClient`
- `list_voices(query=None, category=None, gender=None, accent=None, page=1, limit=50, include_audio_url=True)`
- `get_voice(voice_id, include_audio_url=True)`
- `list_categories()`
- `create_upload_link(filename, file_size, org_id=None)`
- `create_user_voice(name, upload_id, duration, org_id=None, description=None, gender=None, accent=None, tags=None)`
- `get_user_voice_job(job_id)`
- `list_user_voices(org_id=None, search=None, gender=None, accent=None, tags=None, page=1, limit=50)`
- `get_user_voice(voice_id)`
- `update_user_voice(voice_id, name=None, description=None, gender=None, accent=None, tags=None)`
- `delete_user_voice(voice_id)`
- `generate_tts(text, org_id=None, voice_id=None, voice_source=None, voice_s3_key=None, exaggeration=None, cfg_weight=None, temperature=None)`
- `generate_tts_multi_speaker(segments, voices, org_id=None, exaggeration=None, cfg_weight=None, temperature=None, add_silence_between_speakers=True, silence_duration=None)`
- `get_tts_job(job_id, poll=True)`
- `list_tts_jobs(org_id=None, page=1, limit=20, status=None)`

## `voiceover` - `VoiceoverClient`
- `create_voiceover(project_id, voiceover_code=None, **kwargs)`
- `get_voiceover(voiceover_id=None, project_id=None, include_results=True, include_storyboard=False, generate_audio_link=True, **kwargs)`
- `redo_voiceover(voiceover_id=None, project_id=None, voiceover_code=None, **kwargs)`
- `update_voiceover_data(voiceover_id=None, project_id=None, **kwargs)`
- `get_voiceover_history(voiceover_id, page=1, limit=10, **kwargs)`
- `get_generation_history(voiceover_id=None, project_id=None, page=1, limit=20, generate_audio_links=True)`
- `switch_generation(generation_id, voiceover_id=None, project_id=None)`
- `get_voice_types(refresh_cache=False)`
- `upload_voiceover_file(project_id, file_path, voice_name='Custom Voiceover')`
- `add_voiceover_to_project(project_id, file_id, voice_name='Custom Voiceover')`
- `remove_voiceover_from_project(project_id)`
- `download_voiceover(voiceover_id=None, project_id=None, output_path=None)`
- `wait_for_completion(voiceover_id=None, project_id=None, timeout_seconds=300, poll_interval=5)`
- `create_and_wait(project_id, voiceover_code=None, timeout_seconds=300, poll_interval=5)`
- `get_or_create_voiceover(project_id, voiceover_code=None, wait_for_completion=False, timeout_seconds=300)`

